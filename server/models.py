from server import db


class TextFlow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src_text = db.Column(db.Text)
    target_text = db.Column(db.Text)
    speaker = db.Column(db.Text)
    translation_history = db.Column(db.Text)
    translation_status = db.Column(db.Integer)
    text_file_id = db.Column(db.Integer)

    def keys(self):
        return ('id', 'src_text', 'target_text', 'translation_history',
                'translation_status', 'text_file_id')

    def __getitem__(self, item):
        return getattr(self, item)


class SrcFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.Text)
    file_path = db.Column(db.Text)
    src_language = db.Column(db.String(length=10))
    project_id = db.Column(db.Integer)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.Text)
    project_type = db.Column(db.Integer)
    src_language = db.Column(db.String(length=10))