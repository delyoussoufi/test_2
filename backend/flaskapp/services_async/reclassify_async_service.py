import asyncio
from typing import List, Optional, Callable

from flask import current_app

from flaskapp import app_logger
from flaskapp.models import DigitalisatModel, SearchCategoryModel, ClassificationStatus
from flaskapp.models.enums import DigitalisatStatus
from flaskapp.services_async._base_async_service import AsyncQueueOneProducer


class ReclassifyDigitalisateService(AsyncQueueOneProducer):

    def __init__(self, digitalisate_ids: List[str], search_category: Optional[SearchCategoryModel] = None, maxsize=10):
        super().__init__(maxsize=maxsize)
        self._digitalisate_ids = digitalisate_ids
        self._search_category = search_category
        self._all_search_categories = set(SearchCategoryModel.get_categories_without_default())

        self.update: Optional[Callable] = None
        self._classify_digitalisat_job: Optional[Callable] = None
        self._job_counter = 0
        self._app = current_app._get_current_object()

    def register_classification_job(self, func: Callable):
        self._classify_digitalisat_job = func

    async def produce(self, *args) -> None:
        for id_ in self._digitalisate_ids:
            model = DigitalisatModel.find_by_id(id_)
            if not model:
                continue

            _search_category = self._search_category
            if _search_category is None and not model.is_unclassified():
                # If no category is defined gets only the ones with open status excluding unclassified
                black_list = {
                    cs.search_category
                    for cs in model.classifications_status if cs.status != ClassificationStatus.OPEN
                }
                _search_category = list(set(self._all_search_categories).difference(black_list))

            await self.queue.put((model.id, _search_category))

    def _job_with_contex(self, digitalisat_id: str, search_categories: List[SearchCategoryModel]) -> None:
        try:
            with self._app.app_context():
                self._classify_digitalisat_job(
                    digitalisat_model=DigitalisatModel.find_by_id(digitalisat_id),
                    status_during_classification=DigitalisatStatus.RECLASSIFYING,
                    search_categories=search_categories,
                )
        except Exception as e:
            app_logger.error(f"classify_digitalisat_job error:\n {e}")

    async def consume(self) -> None:


        while True:
            digitalisate_id, _search_category = await self.queue.get()

            # TODO test more...transaction erros happens.
            # when send to thread we must wrap the method with an app_context if it uses database transactions.
            # await asyncio.to_thread(
            #     self._job_with_contex,
            #     digitalisat_id=digitalisate_id,
            #     search_categories=_search_category,
            # )

            try:
                self._classify_digitalisat_job(
                    digitalisat_model=DigitalisatModel.find_by_id(digitalisate_id),
                    status_during_classification=DigitalisatStatus.RECLASSIFYING,
                    search_categories=_search_category,
                )
            except Exception as e:
                app_logger.error(f"classify_digitalisat_job error:\n {e}")

            if self.update is not None:
                self.update(self._job_counter+1)
                self._job_counter += 1

            self.queue.task_done()

