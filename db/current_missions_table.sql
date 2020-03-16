CREATE TABLE `current_missions` (
  `mission_id` int(11) DEFAULT NULL,
  `progress` int(11) DEFAULT NULL,
  `player_id` bigint(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
