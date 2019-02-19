from articles.models import Article
from blog_api.factory import app, db
from categories.models import Category
from comments.models import Comment
from likes.models import Like
from roles.models import Role
from routes import blueprint
from subscriptions.models import UserSubscription
from tags.models import Tag
from users.models import User

app.register_blueprint(blueprint, url_prefix='/api')


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return dict(app=app, db=db, User=User, article=Article,
                    tag=Tag, category=Category, comment=Comment, role=Role, like=Like,
                    user_subscription=UserSubscription)

    app.shell_context_processor(shell_context)


register_shellcontext(app)

if __name__ == '__main__':
    app.run(port=8080)
