from pyomo.environ import *


def set(model, name):
    """
    Create a set in a Pyomo model.

    :param model: The Pyomo model to which the set will be added.
    :param name: The name of the set.
    :return: model.name = Set() ::: Set(initialize=initialize)
    """
    setattr(model, name, Set())
    return getattr(model, name)


def s(model, name):
    """
    Create a set in a Pyomo model.

    :param model: The Pyomo model to which the set will be added.
    :param name: The name of the set.
    :return: model.name
    """
    return getattr(model, name)


def par(model, name, time=None, default=None):
    """
    Use to create a parameter in a Pyomo model.

    :param model: The Pyomo model to which the parameter will be added.
    :param name: The name of the parameter.
    :param time: (Optional) The set of time indices for the parameter. If not provided, the parameter is not time-indexed.
    :param default: (Optional) The default value for the parameter. If not provided, the parameter is created without a default value.
    :return: model.name = Param() ::: Param(default=default) ::: Param(time) ::: Param(time, default=default)


    """

    if time is None:
        if default is None:
            setattr(model, name, Param())
            return getattr(model, name)

        setattr(model, name, Param(default=default))
        return getattr(model, name)

    time_idx = getattr(model, time)
    if default is None:
        setattr(model, name, Param(time_idx))
        return getattr(model, name)

    setattr(model, name, Param(time_idx, default=default))
    return getattr(model, name)


def p(model, name):
    """
    Create a parameter in a Pyomo model.

    :param model: The Pyomo model to which the parameter will be added.
    :param name: The name of the parameter.
    :return: model.name
    """
    return getattr(model, name)


def var_pos(model, name, time=None, initialize=None):
    """
    Create a variable in a Pyomo model.

    :param model: The Pyomo model to which the variable will be added.
    :param name: The name of the variable.
    :param time: (Optional) The set of time indices for the variable. If not provided, the variable is not time-indexed.
    :param initialize: (Optional) The initial value for the variable. If not provided, the variable is initialized to what pyomo initializes
    :return: model.name = Var(within=NonNegativeReals) ::: Var(within=NonNegativeReals, initialize=initialize) ::: Var(time, within=NonNegativeReals) ::: Var(time, within=NonNegativeReals, initialize=initialize)
    """
    if time is None:
        if initialize is None:
            setattr(model, name, Var(within=NonNegativeReals))
            return getattr(model, name)

        setattr(model, name, Var(within=NonNegativeReals, initialize=initialize))
        return getattr(model, name)

    time_idx = getattr(model, time)
    if initialize is None:
        setattr(model, name, Var(time_idx, within=NonNegativeReals))
        return getattr(model, name)

    setattr(model, name, Var(time_idx, within=NonNegativeReals, initialize=initialize))
    return getattr(model, name)

def var_bin(model, name, time=None, initialize=None):
    """
    Create a variable in a Pyomo model.

    :param model: The Pyomo model to which the variable will be added.
    :param name: The name of the variable.
    :param time: (Optional) The set of time indices for the variable. If not provided, the variable is not time-indexed.
    :param initialize: (Optional) The initial value for the variable. If not provided, the variable is initialized to what pyomo initializes
    :return: model.name = Var(within=NonNegativeReals) ::: Var(within=NonNegativeReals, initialize=initialize) ::: Var(time, within=NonNegativeReals) ::: Var(time, within=NonNegativeReals, initialize=initialize)
    """
    if time is None:
        if initialize is None:
            setattr(model, name, Var(within=Binary))
            return getattr(model, name)

        setattr(model, name, Var(within=Binary, initialize=initialize))
        return getattr(model, name)

    time_idx = getattr(model, time)
    if initialize is None:
        setattr(model, name, Var(time_idx, within=Binary))
        return getattr(model, name)

    setattr(model, name, Var(time_idx, within=Binary, initialize=initialize))
    return getattr(model, name)

def v(model, name):
    """
    Create a variable in a Pyomo model.

    :param model: The Pyomo model to which the variable will be added.
    :param name: The name of the variable.
    :return: model.name
    """
    return getattr(model, name)
