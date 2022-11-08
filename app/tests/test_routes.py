#  import module_manager
# module_manager.review()

from flask import Flask
import pytest
from app.handlers.routes import configure_routes

def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'

def test_batch_success():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    # Values will be taking a parameter string with _ as sep. variables and , as sep. students
    url = '/batch?applicant_info=18_19_3_4,20_10_4_1'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'0\n'

def test_batch_failed_no_students():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    # Values will be taking a parameter string with _ as sep. variables and , as sep. students
    url = '/batch'

    response = client.get(url)

    assert response.status_code == 500
    # assert response.get_data() == b'\n'
    
def test_batch_failed_incorrect_bounds():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    # Values will be taking a parameter string with _ as sep. variables and , as sep. students
    url = '/batch?applicant_info=18_19_3_300,20_10000_4_34'

    response = client.get(url)

    assert response.status_code == 500
    assert response.get_data() == b'hi your absences parameter is outta bounds.'

def test_batch_failed_too_many_params():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    # Values will be taking a parameter string with _ as sep. variables and , as sep. students
    url = '/batch?applicant_info=18_19_3,20_10_4_10_9'

    response = client.get(url)

    assert response.status_code == 500
    assert response.get_data() == b"hi you're passing in the wrong number of parameters."

def test_batch_failed_not_enough_params():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    # Values will be taking a parameter string with _ as sep. variables and , as sep. students
    url = '/batch?applicant_info=18_19_3,20_10_'

    response = client.get(url)

    assert response.status_code == 500
    assert response.get_data() == b"hi you're passing in the wrong number of parameters."

def test_batch_one_student():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    # Values will be taking a parameter string with _ as sep. variables and , as sep. students
    url = '/batch?applicant_info=18_19_3_3'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'0\n'