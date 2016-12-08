CREATE TABLE `project_list` (
  `project_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `filename` varchar(200) DEFAULT NULL,
  `domain` varchar(100) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `description` text,
  `lang` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`project_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

