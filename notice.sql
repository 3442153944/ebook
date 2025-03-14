/*
 Navicat Premium Data Transfer

 Source Server         : forum
 Source Server Type    : MySQL
 Source Server Version : 80029
 Source Host           : localhost:3306
 Source Schema         : forum

 Target Server Type    : MySQL
 Target Server Version : 80029
 File Encoding         : 65001

 Date: 14/03/2025 15:02:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for notice
-- ----------------------------
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '通知ID',
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '通知标题',
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '通知内容',
  `time` datetime NULL DEFAULT NULL COMMENT '通知时间',
  `send_user_id` int NULL DEFAULT NULL COMMENT '发送者ID',
  `target_user_id` int NULL DEFAULT NULL COMMENT '发送给谁',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notice
-- ----------------------------
INSERT INTO `notice` VALUES (1, '通知测试', '这是一个通知', '2025-03-13 10:30:02', 1, 1);
INSERT INTO `notice` VALUES (2, '通知测试2', '这是一个通知2', '2025-03-13 10:35:40', 1, 1);
INSERT INTO `notice` VALUES (3, '通知测试3', '这是一个通知', '2025-03-13 14:45:44', 184, 1);
INSERT INTO `notice` VALUES (4, '通知测试4', '这是一个通知', '2025-03-13 14:46:24', 184, 1);

SET FOREIGN_KEY_CHECKS = 1;
