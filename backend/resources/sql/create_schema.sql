create table S_ROLES
(
    ROLE_ID varchar(50) not null,
    LABEL varchar(50) not null,
    primary key (ROLE_ID)
);

create table if NOT exists S_RIGHTS (
    RIGHT_ID varchar(50) not null,
    LABEL varchar(100) not null,
    primary key (RIGHT_ID)
);

create table T_ROLES_RIGHTS (
    ROLE_ID varchar(50) not null,
    RIGHT_ID varchar(50) not null,
    primary key (ROLE_ID, RIGHT_ID),
    foreign key (RIGHT_ID) references S_RIGHTS (RIGHT_ID) on delete restrict,
    foreign key (ROLE_ID) references S_ROLES (ROLE_ID) on delete restrict
);


create table if NOT exists  T_APPLICATION_PARAM
(
    PARAM_ID varchar(50) not null,
    LABEL varchar(100) not null,
    PARAM_VALUE varchar(200) not null,
    primary key (PARAM_ID)
);


create table if NOT exists  T_ACCESS_TOKENS (
	ID varchar(16) not null,
	EXPIRY timestamp,
	TOKEN varchar(255) not null,
	USER_ID varchar(16),
	primary key (ID)
);

create table if NOT exists  T_EXCEPTION_LOG (
	ID varchar(16) not null,
	DATE timestamp,
	HASH bigint,
	STACKTRACE varchar(5000),
	TITLE varchar(255),
	primary key (ID)
);

create table if NOT exists  T_USER (
	USER_ID varchar(16) not null,
	FORENAME varchar(50) not null,
	PASSWORD varchar(80) not null,
	SURNAME varchar(50) not null,
	USERNAME varchar(50) not null unique,
	primary key (USER_ID)
);

create table if NOT exists  T_USER_ROLES (
    USER_ID varchar(16) not null,
    ROLE_ID varchar(50) not null,
    LASTCHANGE_BY varchar(16),
    LASTCHANGE_AT timestamp,
    primary key (USER_ID, ROLE_ID),
    foreign key (USER_ID) references T_USER (USER_ID) on delete restrict,
    foreign key (ROLE_ID) references S_ROLES (ROLE_ID) on delete restrict
);

create table T_USER_RIGHTS (
    USER_ID varchar(16) not null,
    RIGHT_ID varchar(50) not null,
    LASTCHANGE_BY varchar(16),
    LASTCHANGE_AT timestamp,
    primary key (USER_ID, RIGHT_ID),
    foreign key (USER_ID) references T_USER (USER_ID) on delete restrict,
    foreign key (LASTCHANGE_BY) references T_USER (USER_ID),
    foreign key (RIGHT_ID) references S_RIGHTS (RIGHT_ID) on delete restrict
);


create table if NOT exists  T_ARCHIVALIEN_ARTEN (
    ID varchar(16) not null,
    SCOPE_ENTRG_TYP_ID varchar(20),
    NAME varchar(200) not null,
    primary key (ID)
);

create table if NOT exists  T_SEARCH_CATEGORY (
    ID varchar(16) not null,
    NAME varchar(255) not null unique,
    DESCRIPTION varchar(255),
    'ORDER' integer not null,
    primary key (ID)
);

create table if NOT exists  T_SEARCH_TERM (
    ID varchar(16) not null,
    CATEGORY_ID varchar(16) not null,
    SEARCH_VALUE varchar(255),
    primary key (ID),
    foreign key (CATEGORY_ID) references T_SEARCH_CATEGORY (ID) on delete restrict
);

create table if NOT exists  T_BLACKLIST_TERM (
    ID varchar(16) not null,
    CATEGORY_ID varchar(16) not null,
    VALUE varchar(255) not null,
    primary key (ID),
    foreign key (CATEGORY_ID) references T_SEARCH_CATEGORY (ID) on delete restrict
);

create table if NOT exists  T_NON_RELEVANT_TERM (
    ID varchar(16) not null,
    CATEGORY_ID varchar(16) not null,
    VALUE varchar(255) not null,
    primary key (ID),
    foreign key (CATEGORY_ID) references T_SEARCH_CATEGORY (ID) on delete restrict
);

create table T_TARGET_FOLDERS
(
    ID varchar(16) not null,
    PATH varchar(400) not null,
    ACTIVE boolean not null,
    primary key (ID)
);

create table T_BESTAND_WATCHER (
    ID varchar(16) not null,
    NAME character varying(400) not null,
    STATUS varchar(50) not null,
	LAST_SYNCHRONIZATION  timestamp,
    primary key (ID)
);

create table T_DIGITALISAT (
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
    foreign key (ARCHIVALIEN_ART_ID) references T_ARCHIVALIEN_ARTEN (ID) on delete restrict,
    foreign key (TARGET_FOLDER_ID) references T_TARGET_FOLDERS (ID) on delete restrict
);

create table T_DIGITALISAT_IMAGE (
    ID varchar(16) not null,
    DIGITALISAT_ID varchar(16) not null,
    NAME character varying(400) not null,
	SHA1 varchar(40) not null,
    IMAGE_ORDER integer not null,
	IMAGE_SIZE  float not null,
    primary key (ID),
    foreign key (DIGITALISAT_ID) references T_DIGITALISAT (ID) on delete restrict
);

create table T_SCOPE_DATA (
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
    foreign key (DIGITALISAT_ID) references T_DIGITALISAT (ID) on delete restrict
);

create table T_DIGITALISAT_IMAGE_OCR (
    DIGITALISAT_IMAGE_ID varchar(16) not null,
    OCR_TEXT text,
    SEARCH_VECTOR tsvector,
    CREATE_DATE date not null,
    primary key (DIGITALISAT_IMAGE_ID),
    foreign key (DIGITALISAT_IMAGE_ID) references T_DIGITALISAT_IMAGE (ID) on delete restrict
);

create table T_CLASSIFICATION_STATUS (
    DIGITALISAT_ID varchar(16) not null,
    SEARCH_CATEGORY_ID varchar(16) not null,
    STATUS varchar(50) not null,
    NUMBER_OF_PAGES_CLASSIFIED integer not null,
    HAS_OWNERSHIP boolean not null,
    HAS_LOCATION boolean not null,
    primary key (DIGITALISAT_ID, SEARCH_CATEGORY_ID),
    foreign key (DIGITALISAT_ID) references T_DIGITALISAT (ID) on delete restrict,
    foreign key (SEARCH_CATEGORY_ID) references T_SEARCH_CATEGORY (ID) on delete restrict
);

create table T_IMAGE_CLASSIFICATION (
    DIGITALISAT_IMAGE_ID varchar(16) not null,
    SEARCH_CATEGORY_ID varchar(16) not null,
    FOUND_TERMS json not null,
    primary key (DIGITALISAT_IMAGE_ID, SEARCH_CATEGORY_ID),
    foreign key (DIGITALISAT_IMAGE_ID) references T_DIGITALISAT_IMAGE (ID) on delete restrict,
    foreign key (SEARCH_CATEGORY_ID) references T_SEARCH_CATEGORY (ID) on delete restrict
);

create table T_DIGITALISAT_COMMENT (
    ID varchar(16) not null,
    DIGITALISAT_ID varchar(16) not null,
    USER_ID varchar(16),
	REFERENCE varchar(100),
    COMMENT varchar(5000) not null,
    POST_DATE timestamp not null,
    COMMENT_LINK_ID varchar(16),
    primary key (ID),
    foreign key (DIGITALISAT_ID) references T_DIGITALISAT (ID) on delete restrict,
    foreign key (USER_ID) references T_USER (USER_ID)
);

create table T_VORGANG (
    ID varchar(16) not null,
    DIGITALISAT_ID varchar(16) not null,
    SEARCH_CATEGORY_ID varchar(16) not null,
    VORGANG_ORDER integer not null,
    CREATE_DATE date not null,
    primary key (ID),
    foreign key (DIGITALISAT_ID) references T_DIGITALISAT (ID) on delete restrict,
    foreign key (SEARCH_CATEGORY_ID) references T_SEARCH_CATEGORY (ID) on delete restrict
);

create table T_VORGANG_IMAGES (
    VORGANG_ID varchar(16) not null,
    DIGITALISAT_IMAGE_ID varchar(16) not null,
    primary key (VORGANG_ID, DIGITALISAT_IMAGE_ID),
    foreign key (VORGANG_ID) references T_VORGANG (ID) on delete restrict,
    foreign key (DIGITALISAT_IMAGE_ID) references T_DIGITALISAT_IMAGE (ID) on delete restrict
);

create table T_CLASSIFYING_JOB (
    ID varchar(50) not null,
    CATEGORY_ID varchar(16),
    STATUS varchar(50) not null,
    START_TIME timestamp not null,
    LAST_UPDATE timestamp not null,
    FILES_PROCESSED int not null,
    TOTAL_FILES int not null,
    primary key (ID),
    foreign key (CATEGORY_ID) references T_SEARCH_CATEGORY (ID) on delete restrict
);

create table T_DIGITALISAT_CLASSIFICATION_LOCK (
    DIGITALISAT_ID varchar(16) not null,
    SEARCH_CATEGORY_ID varchar(16) not null,
    primary key (DIGITALISAT_ID, SEARCH_CATEGORY_ID),
    foreign key (DIGITALISAT_ID) references T_DIGITALISAT (ID) on delete restrict,
    foreign key (SEARCH_CATEGORY_ID) references T_SEARCH_CATEGORY (ID) on delete restrict
);
