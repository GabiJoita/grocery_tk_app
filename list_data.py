import sqlite3


class MyDbList:
    def __init__(self):
        self.con = sqlite3.connect('my_list.db')
        self.crs = self.con.cursor()

    def create_command(self):
        create_command = """
            CREATE TABLE IF NOT EXISTS my_list (
            id INTEGER,
            name TEXT(20),
            category TEXT(20),
            price FLOAT,
            value TEXT(5)
            );
            """
        self.crs.execute(create_command)
        self.con.commit()

    def insert_command(self):
        insert_command = """
            INSERT INTO my_list (id, name, category, price, value) VALUES (1, 'apples', 'fruits', 5.12, 'lei');
            INSERT INTO my_list VALUES(2, 'bread', 'food', 1.5, 'lei');
            INSERT INTO my_list VALUES(3, 'water', 'drink', 0.8, 'lei');
            INSERT INTO my_list VALUES(4, 'juice', 'drink', 4.5, 'lei');
            INSERT INTO my_list VALUES(5, 'meat', 'food', 15.0, 'lei');
            INSERT INTO my_list VALUES(6, 'salad', 'food', 5.5, 'lei');
            """
        self.crs.executescript(insert_command)
        self.con.commit()

    def query_all(self):
        query_all = "SELECT * FROM my_list"
        self.crs.execute(query_all)
        result = self.crs.fetchall()
        self.con.close()
        return result


if __name__ == '__main__':
    my_list = MyDbList()
    my_list.create_command()
    my_list.insert_command()
