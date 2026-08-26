import ast


def generate_revoke_ingress_ast(drift_event):
    """
    Generate an AST for revoke_security_group_ingress()
    using a PUBLIC_INGRESS drift event.
    """

    group_id = drift_event["resource_id"]
    protocol = drift_event["protocol"]
    from_port = drift_event["from_port"]
    to_port = drift_event["to_port"]
    cidr = drift_event["cidr"]

    ip_permission = ast.Dict(
        keys=[
            ast.Constant(value="IpProtocol"),
            ast.Constant(value="FromPort"),
            ast.Constant(value="ToPort"),
            ast.Constant(value="IpRanges"),
        ],
        values=[
            ast.Constant(value=protocol),
            ast.Constant(value=from_port),
            ast.Constant(value=to_port),
            ast.List(
                elts=[
                    ast.Dict(
                        keys=[ast.Constant(value="CidrIp")],
                        values=[ast.Constant(value=cidr)],
                    )
                ],
                ctx=ast.Load(),
            ),
        ],
    )

    revoke_call = ast.Expr(
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="ec2", ctx=ast.Load()),
                attr="revoke_security_group_ingress",
                ctx=ast.Load(),
            ),
            args=[],
            keywords=[
                ast.keyword(
                    arg="GroupId",
                    value=ast.Constant(value=group_id),
                ),
                ast.keyword(
                    arg="IpPermissions",
                    value=ast.List(
                        elts=[ip_permission],
                        ctx=ast.Load(),
                    ),
                ),
            ],
        )
    )

    module = ast.Module(
        body=[revoke_call],
        type_ignores=[],
    )

    return ast.fix_missing_locations(module)