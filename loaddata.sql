CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "emoji" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);
INSERT INTO `Users` VALUES(null, "Walter", "White", "whw@gmail.com", "I am the one who knocks.", "Heisenberg", "ihateskyler", null, 2022, 1);
INSERT INTO `Users` VALUES(null, "Ricky", "Bobby", "rbob@wonderbread.com", "If you ain't first you're last.", "magicman", "iwannagofast", null, 2022, 1);


INSERT INTO `Subscriptions` VALUES(null, 1, 2, 2022);
INSERT INTO `Subscriptions` VALUES(null, 2, 1, 2020);

INSERT INTO `Posts` VALUES(null, 1, 2, "Test", 2022, null, "hello world", 1);

INSERT INTO `Posts` VALUES(null, 2, 4, "Test", 2022, null, "yoooooo", 1);

INSERT INTO `Comments` VALUES(null, 1, 2, "Test");

INSERT INTO `Reactions` VALUES(null, "🔥");
INSERT INTO `Reactions` VALUES(null, "😂");
INSERT INTO `Reactions` VALUES(null, "💯");
INSERT INTO `Reactions` VALUES(null, "💩");
INSERT INTO `Reactions` VALUES(null, "💜");

INSERT INTO `PostReactions` VALUES(null, 1, 2, 1);
INSERT INTO `PostReactions` VALUES(null, 2, 1, 2);


INSERT INTO `Tags` VALUES(null, "Happy");
INSERT INTO `Tags` VALUES(null, "Sad");
INSERT INTO `Tags` VALUES(null, "Motivated");
INSERT INTO `Tags` VALUES(null, "Inspired");
INSERT INTO `Tags` VALUES(null, "Mad");


INSERT INTO `PostTags` VALUES(null, 1, 2);
INSERT INTO `PostTags` VALUES(null, 2, 1);


INSERT INTO `Categories` VALUES(null, "Sports");
INSERT INTO `Categories` VALUES(null, "Technology");
INSERT INTO `Categories` VALUES(null, "Medicine");
INSERT INTO `Categories` VALUES(null, "Weather");
INSERT INTO `Categories` VALUES(null, "Current Events");


        SELECT
            p.id,
            p.user_id,
            p.category_id ,
            p.title ,
            p.publication_date ,
            p.image_url ,
            p.content ,
            p.approved,
            c.label,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active,
            r.emoji,
            t.id tag_id,
            t.label tag_label
        FROM Posts p
        JOIN Categories c
            ON c.id = p.category_id
        JOIN Users u
            ON u.id = p.user_id
        JOIN PostReactions pr
            ON p.id = pr.post_id
        JOIN Reactions r
            ON pr.reaction_id = r.id
        JOIN PostTags pt
            ON p.id = pt.post_id
        JOIN Tags t
            ON pt.tag_id = t.id
          WHERE p.id = 1

        SELECT
            s.id,
            s.follower_id ,
            s.author_id,
            s.created_on,
            u1.first_name follower_first_name,
            u1.last_name follower_last_name,
            u1.email follower_email,
            u1.bio follower_bio,
            u1.username follower_username,
            u1.password follower_password,
            u1.profile_image_url follower_profile_image_url,
            u1.created_on follower_created_on,
            u1.active follower_active,
            u2.first_name author_first_name,
            u2.last_name author_last_name,
            u2.email author_email,
            u2.bio author_bio,
            u2.username author_username,
            u2.password author_password,
            u2.profile_image_url author_profile_image_url,
            u2.created_on author_created_on,
            u2.active author_active,
            p.user_id,
            p.category_id ,
            p.title ,
            p.publication_date ,
            p.image_url ,
            p.content ,
            p.approved
        FROM Subscriptions s
        JOIN Users u1
            ON u1.id = s.follower_id
        JOIN Users u2
            ON u2.id = s.author_id
        JOIN Posts p
            ON p.user_id = s.author_id







