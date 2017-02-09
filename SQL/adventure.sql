-- branch shallin
DROP DATABASE IF EXISTS adventure;
CREATE DATABASE adventure;
USE adventure;

--
-- Table structure for table `users`
--

-- DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`(
  `user_id` int(11) auto_increment,
  `user_name` varchar(200) default NULL,
   PRIMARY KEY  (`user_id`)
); -- ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

-- /*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(0,'Tomer Marx'),
(0,'Shallin Ris');
-- /*!40000 ALTER TABLE `users` ENABLE KEYS */;

--
-- Table structure for table `games`
--


--
-- Dumping data for table `games`
--

-- LOCK TABLES `games` WRITE;
-- /*!40000 ALTER TABLE `games` DISABLE KEYS */;

-- /*!40000 ALTER TABLE `games` ENABLE KEYS */;
-- UNLOCK TABLES;


--
-- Table structure for table `story`
--

-- DROP TABLE IF EXISTS `story`;
CREATE TABLE `story` (
  `id` int(11),
  `user_id` int(11),
  `adventure_id` int(11) default NULL,
  `story_id` int(11) default NULL,
  `question_type` int(11) default NULL,
  `content` varchar(1000) default NULL,
  `life_unit` int(11) default NULL,
  `wealth_unit` int(11) default NULL,
  PRIMARY KEY  (`id`),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
  );

--  KEY `idx_actor_id` (`actor_id`),
--  KEY `idx_movie_id` (`movie_id`)
 -- ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `story`
--

-- LOCK TABLES `story` WRITE;
-- /*!40000 ALTER TABLE `story` DISABLE KEYS */;
INSERT INTO `story` VALUES
(1, 1, 1, 1, 0, 'You wake up late. You:', 0, 0),
(2, 1, 1, 1, 1, 'get ready in a hurry, put on your running shoes and sprint to campus', 50, 10),
(3, 1, 1, 1, 2, 'text Shy that youre running late', 100, 10),
(4, 1, 1, 1, 3, 'dont text anyone and hope that no one notices when you walk in late', 15, 10),
(5, 1, 1, 1, 4, 'throw caution to the wind and decide to skip the entire day', 0, 10),
(6, 1, 1, 2, 0, 'You get to school in the nick of time. You:', 0, 0),
(7, 1, 1, 2, 1, 'walk into class and quietly sit down', 100, 10),
(8, 1, 1, 2, 2, 'hang out in the kitchen talking to your friends and making coffee, despite the fact that Nathalie has told you lecture is starting', 50, 10),
(9, 1, 1, 2, 3, 'stop by cofix because its ok to be a few minutes late', 5, 10),
(10, 1, 1, 2, 4, 'at the sight of 16 Herzl you decide you dont feel like coding today so you turn around and go home', 0, 10),
(11, 1, 1, 3, 0, 'You encounter Shy as you run up the stairs. He asks why you didnt text anyone that you were going to be late.', 0, 0),
(12, 1, 1, 3, 1, 'You apologize and say it wont happen again', 60, 10),
(13, 1, 1, 3, 2, 'You start to cry and then run away', 0, 10),
(14, 1, 1, 3, 3, 'You voluntarily offer to pay the $200 late fee', 100, 10),
(15, 1, 1, 3, 4, 'You tell him that you lost your phone', 0, 10),
(16, 1, 1, 4, 0, 'Youre sitting in class, sipping on coffee, and working on your computer. Someone gets up and knocks your coffee over onto your computer:', 0, 0),
(17, 1, 1, 4, 1, 'You grab another cup of coffee and spill it on their computer', 0, 10),
(18, 1, 1, 4, 2, 'You throw the coffee cup and your ruined computer in the trash', 0, 10),
(19, 1, 1, 4, 3, 'You tell Shy its the other persons fault and that they should pay for the computer damage', 0, 10),
(20, 1, 1, 4, 4, 'You realize that maybe you shouldnt have been drinking coffee in the classroom', 0, 10)
;
-- /*!40000 ALTER TABLE `story` ENABLE KEYS */;
-- UNLOCK TABLES;

-- Table structure for table `adventure`

-- DROP TABLE IF EXISTS `adventure`;
CREATE TABLE `adventure` (
  `adventure_id` int(11),
  `adventure_name` varchar(250) default NULL,
  PRIMARY KEY  (`adventure_id`)
--  KEY `idx_actor_id` (`actor_id`),
--  KEY `idx_movie_id` (`movie_id`)
); -- ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- Dumping data for table `adventure`

-- LOCK TABLES `adventure` WRITE;
-- /*!40000 ALTER TABLE `adventure` DISABLE KEYS */;
INSERT INTO `adventure` VALUES
(1,'Surviving ITC');
-- /*!40000 ALTER TABLE `adventure` ENABLE KEYS */;
-- UNLOCK TABLES;

-- DROP TABLE IF EXISTS `games`;
CREATE TABLE `games` (
  `game_id` int(11) auto_increment,
  `user_id` int(11),
  `adventure_id` int(11) default NULL,
  `user_life` int(11) default NULL,
  `user_money` int(11) default NULL,
  `current_story_id` int(11) default NULL,
  `game_completed` int(11) default NULL,
  PRIMARY KEY (`game_id`),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (adventure_id) REFERENCES adventure(adventure_id)
--  should this be the primary key??
); -- ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `games` VALUES
(0, 1, 1, 100, 10, 4, 1),
(0, 2, 1, 55, 4, 5, 1);

