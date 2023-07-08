# To create a database and configure it:
DB_NAME = "krilya_dets1"
CREATE_DB = "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4'".format(
    DB_NAME
)
USE_DB = "USE {}".format(DB_NAME)
SET_SQL_MODE = "SET sql_mode = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"

# To create tables in database:
TABLES = {}
TABLES["detfond_posts"] = (
    "CREATE TABLE `detfond_posts` ("
    "  `ID` bigint UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `post_author` bigint UNSIGNED NOT NULL DEFAULT 0,"
    "  `post_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',"
    "  `post_date_gmt` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',"
    "  `post_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
    "  `post_title` text(65535) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
    "  `post_excerpt` text(65535) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
    "  `post_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'publish',"
    "  `comment_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'open',"
    "  `ping_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'open',"
    "  `post_password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
    "  `post_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
    "  `to_ping` text(65535) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
    "  `pinged` text(65535) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
    "  `post_modified` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',"
    "  `post_modified_gmt` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',"
    "  `post_content_filtered` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
    "  `post_parent` bigint UNSIGNED NOT NULL DEFAULT 0,"
    "  `guid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
    "  `menu_order` int NOT NULL DEFAULT 0,"
    "  `post_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'post',"
    "  `post_mime_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
    "  `comment_count` bigint NOT NULL DEFAULT 0,"
    "  PRIMARY KEY (`ID`)"
    ") "
)

# INSERT_COORDINATORS_QUERY = f"INSERT INTO customers (ID, post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, post_status) VALUES (%s, %s)"


ID = 17014
post_author = 1
post_date = "2023-06-28 17:00:18"
post_date_gmt = "2023-06-28 14:00:18"
post_content = "html"
post_title = "Бот контакты координаторов"
post_excerpt = None
post_status = "publish"
comment_status = "closed"
ping_status = "closed"
post_password = None
post_name = "bot-kontakty-koordinatorov"
to_ping = None
pinged = None
post_modified = "2023-07-02 22:31:45"
post_modified_gmt = "2023-07-02 19:31:45"
post_content_filtered = None
post_parent = 0
guid = "http://jetrai.online/?page_id=17014"
menu_order = 0
post_type = "page"
post_mime_type = None
comment_count = 0
