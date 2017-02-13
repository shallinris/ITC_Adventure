-- branch shallin
DROP DATABASE IF EXISTS adventure;
CREATE DATABASE adventure;
USE adventure;

CREATE TABLE `users`(
  `user_id` int(11) auto_increment,
  `user_name` varchar(200) default NULL,
   PRIMARY KEY  (`user_id`)
);

CREATE TABLE `images` (
  `image_id` int(11) auto_increment,
  `image_name` varchar(500) default NULL,
  `story_id` int(11),
  `adventure_id` int(11),
  PRIMARY KEY  (`image_id`)
  );

INSERT INTO `images` VALUES
(default, 'inbed.jpg', 1, 1),
(default, 'clock.jpg', 2, 1),
(default, 'stairs.jpg', 3, 1),
(default, 'coffee_and_computer.jpeg', 4, 1),
(default, 'phone_interview.jpg', 1, 2),
(default, 'interview.jpg', 2, 2),
(default, 'salary.jpg', 3, 2),
(default, 'work.jpeg', 4, 2),
(default, 'victory.jpg', 0, 0);

CREATE TABLE `story` (
  `id` int(11),
  `adventure_id` int(11) default NULL,
  `story_id` int(11) default NULL,
  `question_type` int(11) default NULL,
  `content` varchar(1000) default NULL,
  `life_unit` int(11) default NULL,
  `wealth_unit` int(11) default NULL,
  PRIMARY KEY  (`id`)
  );

INSERT INTO `story` VALUES
(1, 1, 1, 0, 'You wake up late. You:', 0, 0),
(2, 1, 1, 1, 'get ready in a hurry, put on your running shoes and sprint to campus', 30, 2),
(3, 1, 1, 2, 'text Shy that youre running late', 10, 0),
(4, 1, 1, 3, 'dont text anyone and hope that no one notices when you walk in late', 90, 4),
(5, 1, 1, 4, 'throw caution to the wind and decide to skip the entire day', 100, 9),
(6, 1, 2, 0, 'You get to school in the nick of time. You:', 0, 0),
(7, 1, 2, 1, 'walk into class and quietly sit down', 10, 0),
(8, 1, 2, 2, 'hang out in the kitchen talking to your friends and making coffee, despite the fact that Nathalie has told you lecture is starting', 50, 4),
(9, 1, 2, 3, 'stop by cofix because its ok to be a few minutes late', 70, 5),
(10, 1, 2, 4, 'at the sight of 16 Herzl you decide you dont feel like coding today so you turn around and go home', 100, 10),
(11, 1, 3, 0, 'You encounter Shy as you run up the stairs. He asks why you didnt text anyone that you were going to be late.', 0, 0),
(12, 1, 3, 1, 'You apologize and say it wont happen again', 30, 1),
(13, 1, 3, 2, 'You start to cry and then run away', 70, 6),
(14, 1, 3, 3, 'You voluntarily offer to pay the $200 late fee', 50, 4),
(15, 1, 3, 4, 'You tell him that you lost your phone', 40, 6),
(16, 1, 4, 0, 'Youre sitting in class, sipping on coffee, and working on your computer. Someone gets up and knocks your coffee over onto your computer:', 0, 0),
(17, 1, 4, 1, 'You grab another cup of coffee and spill it on their computer', 70, 10),
(18, 1, 4, 2, 'You throw the coffee cup and your ruined computer in the trash', 60, 10),
(19, 1, 4, 3, 'You tell Shy its the other persons fault and that they should pay for the computer damage', 60, 5),
(20, 1, 4, 4, 'You realize that maybe you shouldnt have been drinking coffee in the classroom', 10, 4),
(21, 2, 1, 0, 'You finally got your first interview and you get a question you have no idea how to do', 0, 0),
(22, 2, 1, 1, 'You totally break down and tell them you cant do it', 100, 10),
(23, 2, 1, 2, 'You struggle a lot but ask them questions and sort of get the problem right', 50, 4),
(24, 2, 1, 3, 'You struggle a lot but dont talk and dont ask them anything', 80, 6),
(25, 2, 1, 4, 'You tell them why the question they asked is stupid and then you answer your own question', 100, 10),
(26, 2, 2, 0, 'You make it to the second round of interviews', 0, 0),
(27, 2, 2, 1, 'Youre so excited that you spend all night partying and getting wasted', 100, 10),
(28, 2, 2, 2, 'You get to the interview late but then do a pretty good job', 50, 5),
(29, 2, 2, 3, 'You get to the interview early and are not sure how you did, but you did everything ITC trained you to do', 30, 2),
(30, 2, 2, 4, 'You freak out mid interview', 100, 8),
(31, 2, 3, 0, 'You get an offer and need to negotiate salary', 0, 0),
(32, 2, 3, 1, 'You give them a number way below your worth', 50, 10),
(33, 2, 3, 2, 'You tell them to pay you whatever they think is best', 30, 5),
(34, 2, 3, 3, 'You engage in a back and forth with them about a salary you feel is fair', 10, 1),
(35, 2, 3, 4, 'You hire someone to negotiate for you', 100, 10),
(36, 2, 4, 0, 'You got the job! You have your first day of work', 0, 0),
(37, 2, 4, 1, 'You pick an appropriate outfit and get there early', 0, 1),
(38, 2, 4, 2, 'You dont leave much extra time to get there and you show up a little late', 20, 4),
(39, 2, 4, 3, 'You ask if you can work from home because youre really nervous', 50, 8),
(40, 2, 4, 4, 'You take everyone in your new office out to breakfast', 30, 10)
;

CREATE TABLE `adventure` (
  `adventure_id` int(11),
  `adventure_name` varchar(250) default NULL,
  PRIMARY KEY  (`adventure_id`)

);

INSERT INTO `adventure` VALUES
(1,'Surviving ITC'),
(2, 'Getting a Job After ITC');

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

);
