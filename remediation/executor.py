def execute_remediation_ast(ast_tree, ec2_client):
    """
    Execute a validated remediation AST using a controlled scope.
    """

    compiled_code = compile(
        ast_tree,
        filename="<aerodrift-remediation>",
        mode="exec",
    )

    safe_globals = {
        "__builtins__": {},
    }

    safe_locals = {
        "ec2": ec2_client,
    }

    exec(
        compiled_code,
        safe_globals,
        safe_locals,
    )

    return True