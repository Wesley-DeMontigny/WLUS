CREATE TABLE `inventory` (
  `object_id` bigint(20) NOT NULL,
  `lot` int(11) DEFAULT NULL,
  `slot` int(11) DEFAULT NULL,
  `equipped` tinyint(4) DEFAULT NULL,
  `linked` tinyint(4) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `player_id` bigint(20) DEFAULT NULL,
  `proxy_items` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
