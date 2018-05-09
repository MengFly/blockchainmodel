from flask import request


def param_check(params):
    """
    检查所有的参数值，如果参数为Null或者参数长度为0则返回false，
    :param params:要检测的参数列表
    :return:参数列表是否有误，以及有误的参数的位置
    """
    for param in params:
        print(param)
        if param is None or len(param) == 0:
            return True, params.index(param)
    return False, 0


def get_params(params_str):
    """

    :param params_str:
    :return:
    """
    params = []
    for params_str in params_str:
        param = request.form.get(params_str, None)
        params.append(param)
    return params
