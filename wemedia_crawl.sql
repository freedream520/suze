CREATE TABLE `article` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `title` text DEFAULT NULL,
    `content` text DEFAULT NULL,
    `brief` text DEFAULT NULL,
    `cover` text DEFAULT NULL,
    `author` text DEFAULT NULL,
    `url` text DEFAULT NULL,
    `code` text DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
