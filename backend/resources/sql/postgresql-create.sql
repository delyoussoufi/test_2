create schema PROVENANCE;
grant all privileges on schema PROVENANCE to PROVENANCE;

create table if NOT exists  PROVENANCE.S_ROLES
(
    ROLE_ID varchar(50) not null,
    LABEL varchar(50) not null,
    primary key (ROLE_ID)
);
grant all privileges on table PROVENANCE.S_ROLES to PROVENANCE;


insert into PROVENANCE.S_ROLES values ('ROLE_VIEWER','Betrachter') ON CONFLICT ON CONSTRAINT s_roles_pkey DO NOTHING;
insert into PROVENANCE.S_ROLES values ('ROLE_USER','Nutzer') ON CONFLICT ON CONSTRAINT s_roles_pkey DO NOTHING;
insert into PROVENANCE.S_ROLES values ('ROLE_ADMIN','Administrator') ON CONFLICT ON CONSTRAINT s_roles_pkey DO NOTHING;

create table if NOT exists PROVENANCE.S_RIGHTS (
    RIGHT_ID varchar(50) not null,
    LABEL varchar(100) not null,
    primary key (RIGHT_ID)
);
grant all privileges on table PROVENANCE.S_RIGHTS to PROVENANCE;

insert into PROVENANCE.S_RIGHTS values ('RIGHT_DIGITALISATE_VIEW','Digitalisate betrachten') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_SEARCH','Suche') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_COMMENT','Kommentare hinzufügen') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_DIGITALISATE_UPDATE','Digitalisate klassifizieren und deklassifizieren') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_IMAGE_UPDATE','Seiten klassifizieren und deklassifizieren') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_VORGANG','Vorgänge erstellen und löschen') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_VORGANG_PDF','PDF aus Vorgang erstellen') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_CATEGORY_VIEW','Suchkategorieansicht') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_CATEGORY_EDIT','Suchkategorien betrachten') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_USER_EDIT','Nutzer betrachten') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_APP_SETTINGS','Anwendungseinstellungen bearbeiten') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_BESTANDE_ADD','Bestande hinzufügen') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;
insert into PROVENANCE.S_RIGHTS values ('RIGHT_RECLASSIFY','Neu klassifizieren') ON CONFLICT ON CONSTRAINT s_rights_pkey DO NOTHING;

create table if NOT exists PROVENANCE.T_ROLES_RIGHTS (
    ROLE_ID varchar(50) not null,
    RIGHT_ID varchar(50) not null,
    primary key (ROLE_ID, RIGHT_ID),
    foreign key (RIGHT_ID) references PROVENANCE.S_RIGHTS (RIGHT_ID) on delete restrict,
    foreign key (ROLE_ID) references PROVENANCE.S_ROLES (ROLE_ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_ROLES_RIGHTS to PROVENANCE;

insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_DIGITALISATE_VIEW') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_SEARCH') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_COMMENT') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_DIGITALISATE_UPDATE') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_IMAGE_UPDATE') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_VORGANG') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_VORGANG_PDF') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_CATEGORY_VIEW') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_CATEGORY_EDIT') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_USER_EDIT') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_APP_SETTINGS') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_BESTANDE_ADD') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_ADMIN', 'RIGHT_RECLASSIFY') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;

insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_USER', 'RIGHT_DIGITALISATE_VIEW') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_USER', 'RIGHT_SEARCH') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_USER', 'RIGHT_COMMENT') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_USER', 'RIGHT_DIGITALISATE_UPDATE') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_USER', 'RIGHT_IMAGE_UPDATE') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_USER', 'RIGHT_VORGANG') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_USER', 'RIGHT_VORGANG_PDF') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_USER', 'RIGHT_CATEGORY_VIEW') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_USER', 'RIGHT_CATEGORY_EDIT') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;

insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_VIEWER', 'RIGHT_DIGITALISATE_VIEW') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_VIEWER', 'RIGHT_SEARCH') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;
insert into PROVENANCE.T_ROLES_RIGHTS values ('ROLE_VIEWER', 'RIGHT_COMMENT') ON CONFLICT ON CONSTRAINT t_roles_rights_pkey DO NOTHING;


create table if NOT exists  PROVENANCE.T_APPLICATION_PARAM
(
    PARAM_ID varchar(50) not null,
    LABEL varchar(100) not null,
    PARAM_VALUE varchar(200) not null,
    primary key (PARAM_ID)
);
grant all privileges on table PROVENANCE.T_APPLICATION_PARAM to PROVENANCE;

insert into PROVENANCE.T_APPLICATION_PARAM values ('appUrl','Anwendungs-URL', 'http://blha-provenienz.brandenburg.de') ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;
insert into PROVENANCE.T_APPLICATION_PARAM values ('userServiceMail','Benutzerdienst-Mail', 'benutzerdienst@blha.brandenburg.de') ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;
insert into PROVENANCE.T_APPLICATION_PARAM values ('mailSmtpHost','SMTP-Adresse', '10.128.9.41') ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;
insert into PROVENANCE.T_APPLICATION_PARAM values ('title','Scope field for Title', 1) ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;
insert into PROVENANCE.T_APPLICATION_PARAM values ('geburtsname','Scope field for geburtsname', 10158) ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;
insert into PROVENANCE.T_APPLICATION_PARAM values ('dat_findbuch','Scope field for dat_findbuch', 10100) ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;
insert into PROVENANCE.T_APPLICATION_PARAM values ('geburtsdatum','Scope field for geburtsdatum', 4) ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;
insert into PROVENANCE.T_APPLICATION_PARAM values ('geburtsort','Scope field for geburtsort', 10160) ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;
insert into PROVENANCE.T_APPLICATION_PARAM values ('wohnort','Scope field for wohnort', 10164) ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;
insert into PROVENANCE.T_APPLICATION_PARAM values ('registry_signature','Scope field for registry_signature', 18) ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;
insert into PROVENANCE.T_APPLICATION_PARAM values ('associates','Scope field for associates', 8) ON CONFLICT ON CONSTRAINT t_application_param_pkey DO NOTHING;

create table if NOT exists  PROVENANCE.T_ACCESS_TOKENS (
	ID varchar(16) not null,
	EXPIRY timestamp,
	TOKEN varchar(255) not null,
	USER_ID varchar(16),
	primary key (ID)
);
grant all privileges on table PROVENANCE.T_ACCESS_TOKENS to PROVENANCE;

create table if NOT exists  PROVENANCE.T_EXCEPTION_LOG (
	ID varchar(16) not null,
	DATE timestamp,
	HASH bigint,
	STACKTRACE varchar(5000),
	TITLE varchar(255),
	primary key (ID)
);
grant all privileges on table PROVENANCE.T_EXCEPTION_LOG to PROVENANCE;

create table if NOT exists  PROVENANCE.T_USER (
	USER_ID varchar(16) not null,
	FORENAME varchar(50) not null,
	PASSWORD varchar(80) not null,
	SURNAME varchar(50) not null,
	USERNAME varchar(50) not null unique,
	primary key (USER_ID)
);
grant all privileges on table PROVENANCE.T_USER to PROVENANCE;

insert into PROVENANCE.T_USER values ('A7BU1ZBUgL','Bernd', '$2a$10$VO60suFTo90.F/ydH6Ydaud/gZezR0/b79fUeFfUHsccuzZBUzt4y', 'Benutzer', 'user') ON CONFLICT ON CONSTRAINT t_user_pkey DO NOTHING;
insert into PROVENANCE.T_USER values ('FfQMIvHTFQ','Michael', '$2a$10$203UYsnvftbzHSjEoQhGG.1tOWXHuvqGUi04iebeUvAvydN0bAwVS', 'Backmann', 'admin') ON CONFLICT ON CONSTRAINT t_user_pkey DO NOTHING;

create table if NOT exists  PROVENANCE.T_USER_ROLES (
    USER_ID varchar(16) not null,
    ROLE_ID varchar(50) not null,
    LASTCHANGE_BY varchar(16),
    LASTCHANGE_AT timestamp,
    primary key (USER_ID, ROLE_ID),
    foreign key (USER_ID) references PROVENANCE.T_USER (USER_ID) on delete restrict,
    foreign key (ROLE_ID) references PROVENANCE.S_ROLES (ROLE_ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_USER_ROLES to PROVENANCE;

insert into PROVENANCE.T_USER_ROLES values ('A7BU1ZBUgL','ROLE_USER') ON CONFLICT ON CONSTRAINT t_user_roles_pkey DO NOTHING;
insert into PROVENANCE.T_USER_ROLES values ('FfQMIvHTFQ','ROLE_ADMIN') ON CONFLICT ON CONSTRAINT t_user_roles_pkey DO NOTHING;

create table if NOT exists PROVENANCE.T_USER_RIGHTS (
    USER_ID varchar(16) not null,
    RIGHT_ID varchar(50) not null,
    LASTCHANGE_BY varchar(16),
    LASTCHANGE_AT timestamp,
    primary key (USER_ID, RIGHT_ID),
    foreign key (USER_ID) references PROVENANCE.T_USER (USER_ID) on delete restrict,
    foreign key (LASTCHANGE_BY) references PROVENANCE.T_USER (USER_ID),
    foreign key (RIGHT_ID) references PROVENANCE.S_RIGHTS (RIGHT_ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_USER_RIGHTS to PROVENANCE;

insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_DIGITALISATE_VIEW') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ','RIGHT_SEARCH') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_COMMENT') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_DIGITALISATE_UPDATE') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_IMAGE_UPDATE') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_VORGANG') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_VORGANG_PDF') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_CATEGORY_VIEW') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_CATEGORY_EDIT') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_USER_EDIT') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_APP_SETTINGS') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_BESTANDE_ADD') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;
insert into PROVENANCE.T_USER_RIGHTS values ('FfQMIvHTFQ', 'RIGHT_RECLASSIFY') ON CONFLICT ON CONSTRAINT t_user_rights_pkey DO NOTHING;



create table if NOT exists  PROVENANCE.T_ARCHIVALIEN_ARTEN (
    ID varchar(16) not null,
    SCOPE_ENTRG_TYP_ID varchar(20),
    NAME varchar(200) not null,
    primary key (ID)
);
GRANT ALL PRIVILEGES ON PROVENANCE.T_ARCHIVALIEN_ARTEN TO PROVENANCE;

insert into PROVENANCE.T_ARCHIVALIEN_ARTEN values ('FfQMIvHTHI', '00000', 'Unklassifiziert') ON CONFLICT ON CONSTRAINT T_ARCHIVALIEN_ARTEN_PKEY DO NOTHING;
insert into PROVENANCE.T_ARCHIVALIEN_ARTEN values ('FfQMIvHTRT', '10004', 'Akte') ON CONFLICT ON CONSTRAINT T_ARCHIVALIEN_ARTEN_PKEY DO NOTHING;
insert into PROVENANCE.T_ARCHIVALIEN_ARTEN values ('FfQMIvHTRE', '10010', 'Repräsentation') ON CONFLICT ON CONSTRAINT T_ARCHIVALIEN_ARTEN_PKEY DO NOTHING;
insert into PROVENANCE.T_ARCHIVALIEN_ARTEN values ('FfQMIvHTIF', '10014', 'Karte') ON CONFLICT ON CONSTRAINT T_ARCHIVALIEN_ARTEN_PKEY DO NOTHING;
insert into PROVENANCE.T_ARCHIVALIEN_ARTEN values ('FfQMIvHJPG', '10016', 'Foto') ON CONFLICT ON CONSTRAINT T_ARCHIVALIEN_ARTEN_PKEY DO NOTHING;
insert into PROVENANCE.T_ARCHIVALIEN_ARTEN values ('FfQMIvhdgE', '10015', 'Film') ON CONFLICT ON CONSTRAINT T_ARCHIVALIEN_ARTEN_PKEY DO NOTHING;
insert into PROVENANCE.T_ARCHIVALIEN_ARTEN values ('FfQMIvEoRP', '10017', 'Plakat') ON CONFLICT ON CONSTRAINT T_ARCHIVALIEN_ARTEN_PKEY DO NOTHING;
insert into PROVENANCE.T_ARCHIVALIEN_ARTEN values ('FfQMIvWpEK', '10013', 'Urkunde') ON CONFLICT ON CONSTRAINT T_ARCHIVALIEN_ARTEN_PKEY DO NOTHING;
insert into PROVENANCE.T_ARCHIVALIEN_ARTEN values ('FfQMIvHTEA', '10021', 'Entnommene Archivalie') ON CONFLICT  ON CONSTRAINT  T_ARCHIVALIEN_ARTEN_PKEY DO NOTHING;

create table if NOT exists  PROVENANCE.T_SEARCH_CATEGORY (
    ID varchar(16) not null,
    NAME varchar(255) not null unique,
    DESCRIPTION varchar(255),
    'ORDER' integer not null,
    primary key (ID)
);
GRANT ALL PRIVILEGES ON PROVENANCE.T_SEARCH_CATEGORY TO PROVENANCE;

insert into PROVENANCE.T_SEARCH_CATEGORY values ('qSKABGODxEytkdtP', 'Unclassified', 'Default classification when either digitalisat  can''t be classified or no classification were found. ') ON CONFLICT ON CONSTRAINT T_SEARCH_CATEGORY_PKEY DO NOTHING;


create table if NOT exists  PROVENANCE.T_SEARCH_TERM (
    ID varchar(16) not null,
    CATEGORY_ID varchar(16) not null,
    SEARCH_VALUE varchar(255),
    primary key (ID),
    foreign key (CATEGORY_ID) references PROVENANCE.T_SEARCH_CATEGORY (ID) on delete restrict
);
GRANT ALL PRIVILEGES ON PROVENANCE.T_SEARCH_TERM TO PROVENANCE;

create table if NOT exists  PROVENANCE.T_BLACKLIST_TERM (
    ID varchar(16) not null,
    CATEGORY_ID varchar(16) not null,
    VALUE varchar(255) not null,
    primary key (ID),
    foreign key (CATEGORY_ID) references PROVENANCE.T_SEARCH_CATEGORY (ID) on delete restrict
);
GRANT ALL PRIVILEGES ON PROVENANCE.T_BLACKLIST_TERM TO PROVENANCE;

create table if NOT exists  PROVENANCE.T_NON_RELEVANT_TERM (
    ID varchar(16) not null,
    CATEGORY_ID varchar(16) not null,
    VALUE varchar(255) not null,
    primary key (ID),
    foreign key (CATEGORY_ID) references PROVENANCE.T_SEARCH_CATEGORY (ID) on delete restrict
);
GRANT ALL PRIVILEGES ON PROVENANCE.T_NON_RELEVANT_TERM TO PROVENANCE;

create table if NOT exists PROVENANCE.T_TARGET_FOLDERS
(
    ID varchar(16) not null,
    PATH varchar(400) not null,
    ACTIVE boolean not null,
    primary key (ID)
);
grant all privileges on table PROVENANCE.T_TARGET_FOLDERS to PROVENANCE;

create table if NOT exists PROVENANCE.T_BESTAND_WATCHER (
    ID varchar(16) not null,
    NAME character varying(400) not null,
    STATUS varchar(50) not null,
	LAST_SYNCHRONIZATION  timestamp,
    primary key (ID)
);
grant all privileges on table PROVENANCE.T_BESTAND_WATCHER to PROVENANCE;

create table if NOT exists PROVENANCE.T_DIGITALISAT (
    ID varchar(16) not null,
    SCOPE_ID varchar(20),
    FOLDER_NAME character varying(400) not null,
    SIGNATURE character varying(200),
    TARGET_FOLDER_ID varchar not null,
    SUB_FOLDER integer not null,
    ARCHIVALIEN_ART_ID varchar(16),
	EXPECTED_IMAGES integer not null,
	STATUS character varying(50) not null,
    CREATE_DATE date not null,
    DELETE_DATE timestamp,
    primary key (ID),
    foreign key (ARCHIVALIEN_ART_ID) references PROVENANCE.T_ARCHIVALIEN_ARTEN (ID) on delete restrict,
    foreign key (TARGET_FOLDER_ID) references PROVENANCE.T_TARGET_FOLDERS (ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_DIGITALISAT to PROVENANCE;

create table if NOT exists PROVENANCE.T_DIGITALISAT_IMAGE (
    ID varchar(16) not null,
    DIGITALISAT_ID varchar(16) not null,
    NAME character varying(400) not null,
	SHA1 varchar(40) not null,
    IMAGE_ORDER integer not null,
	IMAGE_SIZE  float not null,
    primary key (ID),
    foreign key (DIGITALISAT_ID) references PROVENANCE.T_DIGITALISAT (ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_DIGITALISAT_IMAGE to PROVENANCE;

create table if NOT exists PROVENANCE.T_SCOPE_DATA (
    ID varchar(16) not null,
    DIGITALISAT_ID varchar(16) not null unique,
    TITLE character varying(400),
	GEBURTSNAME varchar(40),
    DAT_FINDBUCH varchar(40),
	GEBURTSDATUM  date,
    GEBURTSORT varchar(40),
    WOHNORT character varying(400),
    REGISTRY_SIGNATURE character varying(200),
    ASSOCIATES character varying(2000),
    primary key (ID),
    foreign key (DIGITALISAT_ID) references PROVENANCE.T_DIGITALISAT (ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_SCOPE_DATA to PROVENANCE;

create table if NOT exists PROVENANCE.T_DIGITALISAT_IMAGE_OCR (
    DIGITALISAT_IMAGE_ID varchar(16) not null,
    OCR_TEXT text,
    SEARCH_VECTOR tsvector,
    CREATE_DATE date not null,
    primary key (DIGITALISAT_IMAGE_ID),
    foreign key (DIGITALISAT_IMAGE_ID) references PROVENANCE.T_DIGITALISAT_IMAGE (ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_DIGITALISAT_IMAGE_OCR to PROVENANCE;

create table if NOT exists PROVENANCE.T_CLASSIFICATION_STATUS (
    DIGITALISAT_ID varchar(16) not null,
    SEARCH_CATEGORY_ID varchar(16) not null,
    STATUS varchar(50) not null,
    NUMBER_OF_PAGES_CLASSIFIED integer not null,
    HAS_OWNERSHIP boolean not null,
    HAS_LOCATION boolean not null,
    primary key (DIGITALISAT_ID, SEARCH_CATEGORY_ID),
    foreign key (DIGITALISAT_ID) references PROVENANCE.T_DIGITALISAT (ID) on delete restrict,
    foreign key (SEARCH_CATEGORY_ID) references PROVENANCE.T_SEARCH_CATEGORY (ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_CLASSIFICATION_STATUS to PROVENANCE;

create table if NOT exists PROVENANCE.T_IMAGE_CLASSIFICATION (
    DIGITALISAT_IMAGE_ID varchar(16) not null,
    SEARCH_CATEGORY_ID varchar(16) not null,
    FOUND_TERMS json not null,
    primary key (DIGITALISAT_IMAGE_ID, SEARCH_CATEGORY_ID),
    foreign key (DIGITALISAT_IMAGE_ID) references PROVENANCE.T_DIGITALISAT_IMAGE (ID) on delete restrict,
    foreign key (SEARCH_CATEGORY_ID) references PROVENANCE.T_SEARCH_CATEGORY (ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_IMAGE_CLASSIFICATION to PROVENANCE;

create table if NOT exists PROVENANCE.T_DIGITALISAT_COMMENT (
    ID varchar(16) not null,
    DIGITALISAT_ID varchar(16) not null,
    USER_ID varchar(16),
	REFERENCE varchar(100),
    COMMENT varchar(5000) not null,
    POST_DATE timestamp not null,
    COMMENT_LINK_ID varchar(16),
    primary key (ID),
    foreign key (DIGITALISAT_ID) references PROVENANCE.T_DIGITALISAT (ID) on delete restrict,
    foreign key (USER_ID) references PROVENANCE.T_USER (USER_ID)
);
grant all privileges on table PROVENANCE.T_DIGITALISAT_COMMENT to PROVENANCE;

create table if NOT exists PROVENANCE.T_VORGANG (
    ID varchar(16) not null,
    DIGITALISAT_ID varchar(16) not null,
    SEARCH_CATEGORY_ID varchar(16) not null,
    VORGANG_ORDER integer not null,
    CREATE_DATE date not null,
    primary key (ID),
    foreign key (DIGITALISAT_ID) references PROVENANCE.T_DIGITALISAT (ID) on delete restrict,
    foreign key (SEARCH_CATEGORY_ID) references PROVENANCE.T_SEARCH_CATEGORY (ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_VORGANG to PROVENANCE;

create table if NOT exists PROVENANCE.T_VORGANG_IMAGES (
    VORGANG_ID varchar(16) not null,
    DIGITALISAT_IMAGE_ID varchar(16) not null,
    primary key (VORGANG_ID, DIGITALISAT_IMAGE_ID),
    foreign key (VORGANG_ID) references PROVENANCE.T_VORGANG (ID) on delete restrict,
    foreign key (DIGITALISAT_IMAGE_ID) references PROVENANCE.T_DIGITALISAT_IMAGE (ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_VORGANG_IMAGES to PROVENANCE;

create table if NOT exists PROVENANCE.T_CLASSIFYING_JOB (
    ID varchar(50) not null,
    CATEGORY_ID varchar(16),
    STATUS varchar(50) not null,
    START_TIME timestamp not null,
    LAST_UPDATE timestamp not null,
    FILES_PROCESSED int not null,
    TOTAL_FILES int not null,
    primary key (ID),
    foreign key (CATEGORY_ID) references PROVENANCE.T_SEARCH_CATEGORY (ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_CLASSIFYING_JOB to PROVENANCE;

create table if NOT exists PROVENANCE.T_DIGITALISAT_CLASSIFICATION_LOCK (
    DIGITALISAT_ID varchar(16) not null,
    SEARCH_CATEGORY_ID varchar(16) not null,
    primary key (DIGITALISAT_ID, SEARCH_CATEGORY_ID),
    foreign key (DIGITALISAT_ID) references PROVENANCE.T_DIGITALISAT (ID) on delete restrict,
    foreign key (SEARCH_CATEGORY_ID) references PROVENANCE.T_SEARCH_CATEGORY (ID) on delete restrict
);
grant all privileges on table PROVENANCE.T_DIGITALISAT_CLASSIFICATION_LOCK to PROVENANCE;
