CREATE TABLE `character` (
  `character_id` bigint(20) NOT NULL,
  `current_name` varchar(45) DEFAULT NULL,
  `requested_name` varchar(45) DEFAULT NULL,
  `head_color` int(11) DEFAULT NULL,
  `head` int(11) DEFAULT NULL,
  `chest_color` int(11) DEFAULT NULL,
  `chest` int(11) DEFAULT NULL,
  `legs` int(11) DEFAULT NULL,
  `hair_style` int(11) DEFAULT NULL,
  `hair_color` int(11) DEFAULT NULL,
  `left_hand` int(11) DEFAULT NULL,
  `right_hand` int(11) DEFAULT NULL,
  `eyebrow_style` int(11) DEFAULT NULL,
  `eye_style` int(11) DEFAULT NULL,
  `mouth_style` int(11) DEFAULT NULL,
  `account_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`character_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
