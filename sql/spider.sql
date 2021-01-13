/*
 Date: 08/01/2021 18:12:56
*/


-- ----------------------------
-- Table structure for spider
-- ----------------------------
DROP TABLE IF EXISTS "public"."spider";
CREATE TABLE "public"."spider" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "title" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "content" text COLLATE "pg_catalog"."default",
  "url" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "imgurl" varchar COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT now(),
  "source" varchar COLLATE "pg_catalog"."default" NOT NULL
)
;
ALTER TABLE "public"."spider" OWNER TO "postgres";
COMMENT ON COLUMN "public"."spider"."source" IS '来源';
COMMENT ON TABLE "public"."spider" IS '爬虫收集表';

-- ----------------------------
-- Primary Key structure for table spider
-- ----------------------------
ALTER TABLE "public"."spider" ADD CONSTRAINT "spider_pkey" PRIMARY KEY ("id");
