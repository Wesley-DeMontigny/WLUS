CREATE TABLE `character_info` (
  `player_id` bigint(20) NOT NULL,
  `position` longtext,
  `rotation` longtext,
  `health` int(11) DEFAULT NULL,
  `max_health` int(11) DEFAULT NULL,
  `armor` int(11) DEFAULT NULL,
  `max_armor` int(11) DEFAULT NULL,
  `imagination` int(11) DEFAULT NULL,
  `max_imagination` int(11) DEFAULT NULL,
  `backpack_space` int(11) DEFAULT NULL,
  `currency` int(11) DEFAULT NULL,
  `universe_score` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  PRIMARY KEY (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
