-- MySQL dump 10.13  Distrib 8.0.16, for osx10.14 (x86_64)
--
-- Host: localhost    Database: bbs
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Language`
--

DROP TABLE IF EXISTS `Language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_time` int(11) DEFAULT NULL,
  `updated_time` int(11) DEFAULT NULL,
  `filedName` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `labelName` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `language` text COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Language`
--

LOCK TABLES `Language` WRITE;
/*!40000 ALTER TABLE `Language` DISABLE KEYS */;
INSERT INTO `Language` VALUES (34,1563374965,1563374965,'createTopic','发表话题','cn'),(35,1563374965,1563374965,'createTopic','新規質問','jp'),(36,1563374965,1563374965,'createTopic','New Topic','en'),(37,1563374965,1563374965,'homepage','Homepage','en'),(38,1563374965,1563374965,'homepage','主页','cn'),(39,1563374965,1563374965,'homepage','ホームページ','jp'),(40,1563374965,1563374965,'blog','ブログ','jp'),(41,1563374965,1563374965,'blog','Blog','en'),(42,1563374965,1563374965,'blog','博客','cn'),(43,1563374965,1563374965,'logout','ログアウト','jp'),(44,1563374965,1563374965,'logout','Signout','en'),(45,1563374965,1563374965,'logout','登出','cn'),(46,1563374965,1563374965,'all_topic','全部のトピック','jp'),(47,1563374965,1563374965,'all_topic','All topic','en'),(48,1563374965,1563374965,'all_topic','全部话题','cn'),(49,1563374965,1563374965,'spin','人気トピック','jp'),(50,1563374965,1563374965,'spin','Hot','en'),(51,1563374965,1563374965,'spin','精品','cn'),(52,1563374965,1563374965,'qa','Q&A','jp'),(53,1563374965,1563374965,'qa','Q&A','en'),(54,1563374965,1563374965,'qa','问答','cn'),(55,1563374965,1563374965,'share','共有','jp'),(56,1563374965,1563374965,'share','Share','en'),(57,1563374965,1563374965,'share','分享','cn'),(58,1563549209,1563549209,'profile','Profile','en'),(59,1563549209,1563549209,'profile','个人信息','cn'),(60,1563549209,1563549209,'profile','プロファイル','jp'),(61,1563549209,1563549209,'score','Score','en'),(62,1563549209,1563549209,'score','积分','cn'),(63,1563549209,1563549209,'score','スコア','jp'),(64,1563549209,1563549209,'signature','这家伙很懒，什么个性签名都没有留下。','cn'),(65,1563549209,1563549209,'signature','Nothing at all','en'),(66,1563549209,1563549209,'signature','何もないよ','jp'),(67,1563549209,1563549209,'delete','Delete','en'),(68,1563549209,1563549209,'delete','削除','jp'),(69,1563549209,1563549209,'delete','删除','cn'),(70,1563699838,1563699838,'author','作者','cn'),(71,1563699838,1563699838,'author','Author','en'),(72,1563699838,1563699838,'author','作者','jp'),(73,1563699838,1563699838,'reply','回复','cn'),(74,1563699838,1563699838,'reply','Reply','en'),(75,1563699838,1563699838,'reply','返事','jp'),(76,1563699838,1563699838,'from','種別','jp'),(77,1563699838,1563699838,'from','From','en'),(78,1563699838,1563699838,'from','来自','cn'),(79,1563701741,1563701741,'publish','Published','jp'),(80,1563701741,1563701741,'publish','Published','en'),(81,1563701741,1563701741,'publish','发布于','cn'),(82,1563701741,1563701741,'viewed','次浏览','cn'),(83,1563701741,1563701741,'viewed','views','en'),(84,1563701741,1563701741,'viewed','回既読','jp'),(85,1563701741,1563701741,'add_reply','添加回复','cn'),(86,1563701741,1563701741,'add_reply','Add reply','en'),(87,1563701741,1563701741,'add_reply','返事する','jp'),(88,1563701741,1563701741,'stairs','楼','cn'),(89,1563701741,1563701741,'stairs','stair','en'),(90,1563701741,1563701741,'stairs','階','jp'),(91,1563702271,1563702271,'ago','Days ago','en'),(93,1563702271,1563702271,'ago','日前','jp'),(94,1563702271,1563702271,'ago','天前','cn'),(95,1563702958,1563702958,'all_blog','全てのブログ','jp'),(96,1563702958,1563702958,'all_blog','全部博客','cn'),(97,1563702958,1563702958,'all_blog','All blogs','en'),(98,1563702958,1563702958,'add_blog','Add blog','en'),(99,1563702958,1563702958,'add_blog','新規ブログ　','jp'),(100,1563702958,1563702958,'add_blog','新建博客','cn'),(101,1563702958,1563702958,'title_more_than_10','标题字数 10 字以上','cn'),(103,1563702958,1563702958,'title_more_than_10','タイトルを10文字以上入力','jp'),(104,1563702958,1563702958,'markdown_note','文章支持 Markdown 语法, 请注意标记代码','cn'),(105,1563702958,1563702958,'markdown_note','You can write article in Markdown','en'),(106,1563702958,1563702958,'markdown_note','Markdown記法が使えます','jp'),(107,1563803090,1563803090,'title_more_than_10','Please input title 10 or more words','en'),(108,1563803090,1563803090,'update','Update','en'),(109,1563803090,1563803090,'update','更新','jp'),(110,1563803090,1563803090,'update','更新','cn'),(111,1563803090,1563803090,'edit','Edit','en'),(112,1563803090,1563803090,'edit','編集','jp'),(113,1563803090,1563803090,'edit','编辑','cn'),(114,1563803090,1563803090,'add_comment','Add comment','en'),(116,1563803090,1563803090,'add_comment','コメント追加','jp'),(117,1563803090,1563803090,'add_comment','添加评论','cn'),(118,1563803090,1563803090,'comment','评论','cn'),(120,1563803090,1563803090,'comment','コメント','jp'),(121,1563803090,1563803090,'comment','Comment','en'),(122,1563804095,1563804095,'choose_board','选择板块','cn'),(123,1563804095,1563804095,'choose_board','Choose board','en'),(124,1563804095,1563804095,'choose_board','板を選択','jp');
/*!40000 ALTER TABLE `Language` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-27  0:16:32
