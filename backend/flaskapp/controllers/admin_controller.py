from typing import List

from flaskapp import app_utils, app_logger
from flaskapp.controllers import admin
from flaskapp.http_util import response as response
from flaskapp.http_util.decorators import secure, query, post
from flaskapp.http_util.exceptions import AppException, EntityNotFound
from flaskapp.models import ExceptionLogModel, Role, ApplicationParamModel, TargetFolderModel, DigitalisatModel, \
    BestandWatcherModel, Right
from flaskapp.search import ExceptionSearch, SearchBestandSearch
from flaskapp.structures.structures import SearchResult, SystemDiskInfo
from flaskapp.utils import FileUtils


@admin.route("applicationParams", methods=["GET"])
@secure(Right.APP_SETTINGS)
def get_application_params():
    application_params: List[ApplicationParamModel] = ApplicationParamModel.get_all()
    return response.model_to_response(application_params)


@admin.route("applicationParams/<string:_id>", methods=["GET"])
@secure(Right.APP_SETTINGS)
def get_application_param(_id: str):
    application_param: ApplicationParamModel = ApplicationParamModel.find_by_id(_id)
    return response.model_to_response(application_param)


@admin.route("applicationParams", methods=["PUT"])
@secure(Right.APP_SETTINGS)
@post(class_to_map=ApplicationParamModel)
def update_application_param(application_param_model: ApplicationParamModel):
    if application_param_model:
        if not application_param_model.label:
            raise AppException("Der Anwendungsparameter muss einen Namen haben.")
        if not application_param_model.param_value:
            raise AppException("Der Anwendungsparameter muss einen Wert haben.")
        existing_model = ApplicationParamModel.find_by_id(application_param_model.param_id)
        if not existing_model:
            raise AppException("Der Anwendungsparameter konnte nicht gefunden werden.")
        existing_model << application_param_model
        existing_model.save()
        return response.model_to_response(existing_model)
    raise AppException("Fehler beim Aktualisieren des Anwendungsparameters.")


@admin.route("/diskInfo", methods=["GET"])
@secure(Right.APP_SETTINGS)
def disk_info():
    active_target_folder = TargetFolderModel.find_active_target_folder()
    if active_target_folder:
        total, used, free = FileUtils.get_disk_info(active_target_folder.path)
        system_info = SystemDiskInfo(totalDiskSpace=total, usedDiskSpace=used, availableDiskSpace=free)
    else:
        raise AppException("Kein aktives Zielverzeichnis definiert.")

    return response.model_to_response(system_info)


@admin.route("/targetFolders", methods=["GET"])
@secure(Right.APP_SETTINGS)
def target_folders():
    target_folders_model: List[TargetFolderModel] = TargetFolderModel.get_all()
    return response.model_to_response(target_folders_model)


@admin.route("/targetFolders/create", methods=["POST"])
@secure(Right.APP_SETTINGS)
@post(class_to_map=TargetFolderModel)
def create_target_folder(target_folder: TargetFolderModel):
    target_folder.id = app_utils.generate_id(16)
    target_folder.active = False
    target_folder.save()
    return response.model_to_response(target_folder)


@admin.route("/saveTargetFolder", methods=["POST"])
@secure(Right.APP_SETTINGS)
@post(class_to_map=TargetFolderModel)
def save_target_folder(target_folder: TargetFolderModel):
    target_folder = TargetFolderModel.update_target_folder(target_folder)
    return response.model_to_response(target_folder)


@admin.route("/targetFolders/activate/<string:folder_id>", methods=["POST"])
@secure(Right.APP_SETTINGS)
def activate_target_folder(folder_id: str):
    if folder_id:
        folders: [TargetFolderModel] = TargetFolderModel.get_all()
        active_folders = 0
        for folder in folders:
            if folder_id == folder.id:
                folder.active = True
                active_folders += 1
            else:
                folder.active = False
        if active_folders > 1:
            raise AppException("Es kann nur ein Zielverzeichnis aktiviert werden!")
        elif active_folders == 0:
            raise AppException("Es konnte kein Zielverzeichnis aktiviert werden!")
        for folder in folders:
            folder.save()
    return response.model_to_response(TargetFolderModel.get_all())


@admin.route("/targetFolders/<string:folder_id>", methods=["DELETE"])
@secure(Right.APP_SETTINGS)
def delete_target_folder(folder_id: str):
    if not folder_id:
        raise AppException("Das Zielverzeichnis konnte nicht gefunden werden.")
    digitalisate: [DigitalisatModel] = DigitalisatModel.find_digitalisate_by_target_folder_id(folder_id)
    if digitalisate and len(digitalisate) > 0:
        raise AppException("Das Zielverzeichnis beinhaltet noch Digitalisate und kann nicht gelöscht werden.")
    target_folder: TargetFolderModel = TargetFolderModel.find_by_id(folder_id)
    if not target_folder:
        raise AppException("Das Zielverzeichnis konnte nicht gefunden werden.")
    if target_folder.active:
        raise AppException("Das Zielverzeichnis ist aktiv und kann nicht gelöscht werden.")
    return response.bool_to_response(target_folder.delete())


@admin.route("/exceptions/all", methods=["GET"])
@secure(Role.ADMIN)
def all_exceptions():
    search_result: SearchResult = ExceptionLogModel.search(ExceptionSearch())
    return response.model_to_response(search_result)


@admin.route("/exceptions/search", methods=["GET"])
@secure(Role.ADMIN)
@query(ExceptionSearch)
def search_exceptions(exception_search: ExceptionSearch):
    search_result: SearchResult = ExceptionLogModel.search(exception_search)
    return response.model_to_response(search_result)


@admin.route("/exceptions/<string:model_id>", methods=["GET"])
@secure(Role.ADMIN)
def exception(model_id: str):
    model: ExceptionLogModel = ExceptionLogModel.find_by_id(model_id)
    if not model:
        raise AppException("Der Fehler konnte nicht gefunden werden!")
    return response.model_to_response(model)


@admin.route("/searchBestaende/search", methods=["GET"])
@secure(Right.BESTANDE_ADD)
@query(SearchBestandSearch)
def search_bestaende(bestand_search: SearchBestandSearch):
    search_result: SearchResult = BestandWatcherModel.search(bestand_search)
    return response.model_to_response(search_result)


@admin.route("/searchBestaende/<string:search_bestand_id>", methods=["GET"])
@secure(Right.BESTANDE_ADD)
def get_search_bestand(search_bestand_id: str):
    search_bestand_model: BestandWatcherModel = BestandWatcherModel.find_by_id(search_bestand_id)
    if search_bestand_model is None:
        raise EntityNotFound("Der Suchbestand konnte nicht ermittelt werden!")

    return response.model_to_response(search_bestand_model)


@admin.route("/searchBestaende", methods=["POST"])
@secure(Right.BESTANDE_ADD)
@post(class_to_map=BestandWatcherModel)
def create_search_bestand(bestand_model: BestandWatcherModel):
    if not bestand_model.id:
        raise AppException("Keine Id für den Bestand erfasst!")
    if not bestand_model.name:
        raise AppException("Kein Name für den Bestand erfasst!")
    # bestand_model.last_synchronization = datetime.now()
    bestand_model.save()
    return response.model_to_response(bestand_model)


@admin.route("/searchBestaende/<string:search_bestand_id>", methods=["DELETE"])
@secure(Right.BESTANDE_ADD)
def delete_bestand(search_bestand_id: str):
    search_bestand_model: BestandWatcherModel = BestandWatcherModel.find_by_id(search_bestand_id)
    if search_bestand_model is None:
        raise EntityNotFound(f"Der Suchbestand {search_bestand_id} konnte nicht gefunden werden.")
    deleted = search_bestand_model.delete()
    if deleted:
        app_logger.info(f"Der Suchbestand {search_bestand_id} wurde gelöscht.")
    else:
        app_logger.warning(f"Der Suchbestand {search_bestand_id} konnte nicht gelöscht werden.")
    return response.bool_to_response(deleted)


@admin.route("/searchBestaende/pauseBestand", methods=["POST"])
@secure(Right.BESTANDE_ADD)
@post("search_bestand_id", "pause")
def pause_bestand(search_bestand_id: str, pause: bool):
    bestand_model: BestandWatcherModel = BestandWatcherModel.find_by_id(search_bestand_id)
    if bestand_model:
        if pause:
            return response.bool_to_response(bestand_model.pause())
        else:
            return response.bool_to_response(bestand_model.unpause())

    return response.bool_to_response(False)
