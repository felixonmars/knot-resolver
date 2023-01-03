import argparse
import json
from typing import List, Optional, Tuple, Type

from knot_resolver_manager.cli.command import Command, CommandArgs, CompWords, register_command
from knot_resolver_manager.datamodel.config_schema import KresConfig


@register_command
class SchemaCommand(Command):
    def __init__(self, namespace: argparse.Namespace) -> None:
        super().__init__(namespace)
        self.file: Optional[str] = namespace.file

    @staticmethod
    def register_args_subparser(
        subparser: "argparse._SubParsersAction[argparse.ArgumentParser]",
    ) -> Tuple[argparse.ArgumentParser, "Type[Command]"]:
        schema = subparser.add_parser(
            "schema", help="Reads JSON-schema repersentation of the configuration directly from the running resolver."
        )
        schema.add_argument("file", help="Optional, file where to export JSON-schema.", nargs="?", default=None)
        return schema, SchemaCommand

    @staticmethod
    def completion(args: List[str], parser: argparse.ArgumentParser) -> CompWords:
        return {}

    def run(self, args: CommandArgs) -> None:
        schema = json.dumps(KresConfig.json_schema(), indent=4)

        if self.file:
            with open(self.file, "w") as f:
                f.write(schema)
        else:
            print(schema)
