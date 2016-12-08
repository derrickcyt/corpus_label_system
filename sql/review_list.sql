CREATE TABLE `review_list` (
  `review_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `project_id` int(11) NOT NULL,
  `is_labeled` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`review_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1368001 DEFAULT CHARSET=utf8;

