DROP TABLE IF EXISTS `weibo_user`;
CREATE TABLE `weibo_user` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `crawl_time` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `weibo_weibo`;
CREATE TABLE `weibo_weibo` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `weibo_id` varchar(50) NOT NULL,
  `text` varchar(5000) NOT NULL,
  `reposts_count` int(10) NOT NULL,
  `comments_count` int(10) NOT NULL,
  `attitudes_count` int(10) NOT NULL,
  `created_at` varchar(20) NOT NULL,
  `crawl_time` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;