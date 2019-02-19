import datetime
import random
import sys
from operator import or_

import faker
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.expression import func

from articles.models import Article
from blog_api.factory import db, bcrypt
from categories.models import Category
from comments.models import Comment
from likes.models import Like
from roles.models import Role, UserRole
from subscriptions.models import UserSubscription
from tags.models import Tag
from users.models import User

faker = faker.Faker()
tags = []
categories = []


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


def encrypt_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def seed_admin():
    role, created = get_or_create(db.session, Role, defaults={'description': 'for admin only'},
                                  name='ROLE_ADMIN')

    admins = User.query.filter(User.users_roles.any(role_id=role.id)).all()
    admins = User.query.filter(User.roles.any(id=role.id)).all()
    admin_count = User.query.filter(User.roles.any(id=role.id)).count()

    user, created = get_or_create(db.session, User, defaults={'first_name': 'adminFN',
                                                              'last_name': 'adminFN',
                                                              'email': 'admin@flaskblogapi.app',
                                                              'password': bcrypt.generate_password_hash('password')},
                                  **{'username': 'admin'})
    # db.session.add(user)

    db.session.commit()

    if len(user.roles) == 0:
        # user.users_roles.append(UserRole(user_id=user.id, role_id=role.id))
        user.roles.append(role)
        db.session.commit()

    # User.query.filter(User.roles.any(name='ROLE_ADMIN')).all()
    # User.query.join(User.roles).filter_by(name='ROLE_ADMIN').all()


def seed_authors():
    role, created = get_or_create(db.session, Role, defaults={'description': 'for authors only'},
                                  name='ROLE_AUTHOR')

    authors_count = db.session.query(User.id).filter(User.roles.any(id=role.id)).count()
    authors_count = User.query.filter(User.roles.any(id=role.id)).count()
    authors_to_seed = 5
    authors_to_seed -= authors_count

    for i in range(0, authors_to_seed):
        profile = faker.profile(fields='username,mail,name')
        username = profile['username']
        first_name = profile['name'].split()[0]
        last_name = profile['name'].split()[1]
        email = profile['mail']
        password = bcrypt.generate_password_hash('password')
        user = User(username=username, first_name=first_name, last_name=last_name, email=email,
                    password=password, roles=[role])
        db.session.add(user)
        db.session.commit()
        # db.session.add(UserRole(user_id=user.id, role_id=role.id))

    db.session.commit()


def seed_users():
    role, created = get_or_create(db.session, Role, defaults={'description': 'for standard users'},
                                  name='ROLE_USER')
    db.session.commit()
    non_user_ids = db.session.query(User.id).filter(
        ~User.roles.any(id=role.id)).all()

    all_users_count = db.session.query(func.count(User.id)).all()[0][0]
    all_users_count = db.session.query(User.id).count()

    # User.query.filter(User.roles.any(UserRole.role_id.in_([1,2]))).count()
    standard_users_count = db.session.query(User).filter(User.roles.any(UserRole.role_id.in_([role.id]))).count()
    standard_users_count = db.session.query(User.id).filter(
        User.roles.any(id=role.id)).count()

    users_to_seed = 23
    users_to_seed -= standard_users_count
    sys.stdout.write('[+] Seeding %d users\n' % users_to_seed)

    for i in range(0, users_to_seed):
        profile = faker.profile(fields='username,mail,name')
        username = profile['username']
        first_name = profile['name'].split()[0]
        last_name = profile['name'].split()[1]
        email = profile['mail']
        password = bcrypt.generate_password_hash('password')
        user = User(username=username, first_name=first_name, last_name=last_name, email=email,
                    password=password)
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()

    db.session.commit()


def seed_tags():
    sys.stdout.write('[+] Seeding tags\n')
    tag = get_or_create(db.session, Tag, defaults={'description': 'rails tutorials'}, name='Ruby On Rails')[0]
    tags.append(tag)

    tag = get_or_create(db.session, Tag, defaults={'description': 'untagged tutorials'}, name='Untagged')[0]
    tags.append(tag)

    tag = get_or_create(db.session, Tag, defaults={'description': 'spring boot tutorials'}, name='Spring Boot')[0]
    tags.append(tag)

    tag = get_or_create(db.session, Tag, defaults={'description': 'laravel tutorials'}, name='Laravel')[0]
    tags.append(tag)

    tag = get_or_create(db.session, Tag, defaults={'description': 'spring boot tutorials'}, name='Spring Boot')[0]
    tags.append(tag)

    tag = get_or_create(db.session, Tag, defaults={'description': 'angular tutorials'}, name='Angular')[0]
    tags.append(tag)

    db.session.add_all(tags)
    db.session.commit()


def seed_categories():
    sys.stdout.write('[+] Seeding categories\n')

    category = get_or_create(db.session, Category, defaults={'description': 'uncategorized tutorials'},
                             name='Uncategorized')[0]
    categories.append(category)

    category = get_or_create(db.session, Category, defaults={'description': 'Java tutorials'}, name='Java')[0]
    categories.append(category)

    category = get_or_create(db.session, Category, defaults={'description': 'ruby tutorials'}, name='Ruby')[0]
    categories.append(category)

    category = get_or_create(db.session, Category, defaults={'description': 'python tutorials'}, name='Python')[0]
    categories.append(category)

    category = get_or_create(db.session, Category,
                             defaults={'description': 'javascript tutorials'}, name='Javascript')[0]
    categories.append(category)

    category = get_or_create(db.session, Category, defaults={'description': 'angular tutorials'}, name='Angular')[0]
    categories.append(category)

    db.session.add_all(categories)
    db.session.commit()


def seed_articles():
    roles = db.session.query(Role.id).filter(or_(Role.name == 'ROLE_ADMIN', Role.name == 'ROLE_AUTHOR')).all()
    # Not working roles = db.session.query(Role.id).filter(Role.name == v for v in ('ROLE_ADMIN', 'ROLE_AUTHOR')).all()
    roles = [role[0] for role in roles]

    articles_count = db.session.query(func.count(Article.id)).all()[0][0]
    articles_to_seed = 23
    articles_to_seed -= articles_count
    sys.stdout.write('[+] Seeding %d articles\n' % articles_to_seed)
    author_admin_ids = [user[0] for user in
                        db.session.query(User.id).filter(User.roles.any(UserRole.role_id.in_(roles))).all()]
    tag_ids = [tag[0] for tag in db.session.query(Tag.id).all()]
    category_ids = [category[0] for category in db.session.query(Category.id).all()]

    for i in range(articles_count, articles_to_seed):
        title = faker.sentence()
        description = '\n'.join(faker.sentences(2))
        body = faker.text()
        user_id = random.choice(author_admin_ids)

        start_date = datetime.date(year=2017, month=1, day=1)
        random_date = faker.date_between(start_date=start_date, end_date='+4y')
        publish_on = random_date
        a = Article(title=title, body=body, description=description, user_id=user_id,
                    publish_on=publish_on)

        a.tags.append(db.session.query(Tag).order_by(func.random()).first())

        for i in range(0, random.randint(1, 2)):
            a.tags.append(random.choice(tags))

        for i in range(0, random.randint(1, 2)):
            a.categories.append(random.choice(categories))

        db.session.add(a)
        db.session.commit()


def seed_comments():
    comments_count = db.session.query(func.count(Comment.id)).scalar()
    comments_to_seed = 31
    comments_to_seed -= comments_count
    sys.stdout.write('[+] Seeding %d comments\n' % comments_to_seed)
    comments = []

    user_ids = [user[0] for user in User.query.with_entities(User.id).all()]
    article_ids = [article[0] for article in Article.query.with_entities(Article.id)]
    # equivalent:
    # user_ids = [user[0] for user in db.session.query(User.id).all()]
    # article_ids = [article[0] for article in db.session.query(Article.id).all()]

    for i in range(comments_count, comments_to_seed):
        user_id = random.choice(user_ids)
        article_id = random.choice(article_ids)
        comments.append(Comment(article_id=article_id,
                                user_id=user_id,
                                content=faker.sentence()))

    db.session.add_all(comments)
    db.session.commit()


def seed_likes():
    likes_count = db.session.query(func.count(Like.id)).scalar()
    likes_to_seed = 30
    user_ids = [user[0] for user in db.session.query(User.id).all()]
    article_ids = [article[0] for article in db.session.query(Article.id).all()]
    for i in range(likes_count, likes_to_seed):
        user_id = random.choice(user_ids)
        liked_article_ids = [user[0] for user in
                             Like.query.filter_by(user_id=user_id).with_entities(Like.article_id).all()]
        non_liked_articles = [a[0] for a in
                              db.session.query(Article.id).filter(Article.id.notin_(liked_article_ids)).all()]
        # Article.id.notin_ same as ~Article.id.in_
        if len(non_liked_articles) == 0:
            sys.stdout.write('This user liked all articles')
            pass
        article_id = random.choice(non_liked_articles)
        db.session.add(Like(user_id=user_id, article_id=article_id))

    db.session.commit()


def seed_subscriptions():
    subscriptions = db.session.query(func.count(UserSubscription.following_id)).scalar()
    subscriptions_to_seed = 30
    user_ids = [user[0] for user in db.session.query(User.id).all()]
    for i in range(subscriptions, subscriptions_to_seed):
        follower_id = random.choice(user_ids)
        already_following_ids = [u[0] for u in UserSubscription.query.filter(
            UserSubscription.follower_id == follower_id).with_entities(UserSubscription.following_id)]
        already_following_ids.append(follower_id)
        user_ids_not_following = set(user_ids).difference(set(already_following_ids))
        following_id = random.sample(user_ids_not_following, 1)[0]
        db.session.add(UserSubscription(following_id=following_id, follower_id=follower_id))
    db.session.commit()


if __name__ == '__main__':
    seed_admin()
    seed_authors()
    seed_users()
    seed_tags()
    seed_categories()
    seed_articles()
    seed_comments()
    seed_likes()
    seed_subscriptions()
