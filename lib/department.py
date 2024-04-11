from __init__ import CURSOR, CONN


class Department:

    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Department instances """
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Department instances """
        sql = """
            DROP TABLE IF EXISTS departments;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and location values of the current Department instance.
        Update object id attribute using the primary key value of new row.
        """
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, location):
        """ Initialize a new Department instance and save the object to the database """
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the table row corresponding to the current Department instance."""
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Department instance"""
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and location values of the current Department instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    
    @classmethod
    def instance_from_db(cls, row):
        """테이블 행의 데이터를 바탕으로 객체 인스턴스를 생성하고 반환합니다."""

        department = cls.all.get(row[0])  # 딕셔너리에서 객체를 검색합니다.
        if department:
            # 객체가 이미 존재하면, 속성 값을 업데이트합니다.
            department.name = row[1]
            department.location = row[2]
        else:
            # 객체가 없으면 새로 생성하고 딕셔너리에 추가합니다.
            department = cls(row[1], row[2])
            department.id = row[0]
            cls.all[department.id] = department

        return department
    
    @classmethod
    def get_all(cls):
        """데이터베이스의 모든 행을 Department 객체로 반환합니다."""

        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """주어진 ID에 해당하는 Department 객체를 반환합니다."""

        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()

        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        """주어진 이름과 일치하는 첫 번째 Department 객체를 반환합니다."""

        sql = "SELECT * FROM departments WHERE name is ?"
        row = CURSOR.execute(sql, (name,)).fetchone()

        return cls.instance_from_db(row) if row else None
    
    def delete(self):
        """현재 Department 인스턴스에 해당하는 테이블 행을 삭제하고,
        딕셔너리 항목을 삭제한 후 id 속성을 다시 할당합니다"""

        sql = """
            DELETE FROM departments
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # id를 키로 사용하여 딕셔너리 항목을 삭제합니다.
        del type(self).all[self.id]

        # id를 None으로 설정합니다.
        self.id = None