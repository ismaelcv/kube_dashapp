from dashapp_skeleton.main import generic_function


def test_lambda_runs() -> None:
    """
    Test to assert that the lambda run correctly
    """

    response = generic_function()

    assert response["statusCode"] == 200
