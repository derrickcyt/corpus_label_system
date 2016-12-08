/*
Navicat MySQL Data Transfer

Source Server         : 203
Source Server Version : 50173
Source Host           : 110.64.66.203:3306
Source Database       : corpus_label

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2016-12-08 17:37:27
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `project_type_list`
-- ----------------------------
DROP TABLE IF EXISTS `project_type_list`;
CREATE TABLE `project_type_list` (
  `type_id` int(11) NOT NULL DEFAULT '0',
  `type_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of project_type_list
-- ----------------------------
INSERT INTO `project_type_list` VALUES ('1', '意见挖掘');
INSERT INTO `project_type_list` VALUES ('2', '一般');
