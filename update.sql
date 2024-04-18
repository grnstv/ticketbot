CREATE FUNCTION create_some_database()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO "database3" ("date", "company_title", "company_address", "user", "title")
    SELECT NEW."date", Db2.title, Db2.address, NEW."user", NEW."title"
    FROM database2 Db2
    WHERE Db2.id = NEW."company_id";

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


CREATE OR REPLACE TRIGGER database1_notion_updates
	AFTER INSERT OR UPDATE
	ON "database1"
	FOR EACH ROW
	EXECUTE PROCEDURE update_some_database()
