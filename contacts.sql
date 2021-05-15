Create DATABASE Contacts;

USE Contacts;

CREATE TABLE `contactbook` (
  `id` int(11) NOT NULL,
  `FirstName` varchar(20) CHARACTER SET utf8 NOT NULL,
  `LastName` varchar(20) CHARACTER SET utf8 NOT NULL,
  `Email` varchar(254) CHARACTER SET utf8 NOT NULL,
  `Phone` varchar(15) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `email` varchar(254) NOT NULL,
  `role` varchar(10) NOT NULL DEFAULT 'user',
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `users` (`user_id`, `email`, `role`, `password`) VALUES
(1, 'admin@gmail.com', 'admin', 'adminpw1234'),
(2, 'user@gmail.com', 'user', 'userpw1234');

ALTER TABLE `contactbook`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);


ALTER TABLE `contactbook`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

