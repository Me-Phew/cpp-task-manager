import click
from click import progressbar
import glob
from utils import does_file_exist, get_first_number_from_string, Task

# Generation constants


TASK_PAYLOAD = """int main() {{

}}
"""

TASK_PAYLOAD_WITH_IOSTREAM = """#include <iostream>

int main() {{

}}
"""

DEFAULT_TASK_FILE_NAME = "{prefix} {task_num}.cpp"
DEFAULT_TASK_FILE_NAME_PREFIX = "Task"

# Merge constants


DEFAULT_TASK_NAME = "{prefix} #{task_num}"
DEFAULT_TASK_NAME_PREFIX = DEFAULT_TASK_FILE_NAME_PREFIX

DEFAULT_LEFT_PADDING_LENGTH = 2


@click.group()
@click.version_option("1.0.0", "--version", "-v", prog_name="C++ Task Manager")
def cli():
    # Default CLI group

    pass


@cli.command()
@click.argument("num_tasks", type=int)
@click.option("--force", "-f", is_flag=True, help="Overwrite any existing files")
@click.option(
    "--ignore-file-extension",
    is_flag=True,
    help="Do not add .cpp extension if a custom task name template does not have it",
)
@click.option(
    "--include-iostream",
    "--io",
    is_flag=True,
    help="Whether to include iostream library in payload",
)
@click.option(
    "--task-name-template",
    "-t",
    type=click.STRING,
    default=DEFAULT_TASK_FILE_NAME,
    help=f'Default: "{DEFAULT_TASK_FILE_NAME}",'
    f" placeholders: {{task_num}} - required, {{prefix}} - optional",
)
@click.option(
    "--task-name-prefix",
    "-p",
    type=click.STRING,
    default=None,
    help=f'Default: "{DEFAULT_TASK_FILE_NAME_PREFIX}"',
)
def generate(
    num_tasks,
    force,
    ignore_file_extension,
    include_iostream,
    task_name_template,
    task_name_prefix,
):
    if task_name_template.find("{task_num}") == -1:
        raise click.UsageError(
            "Task name template has to include {task_num} placeholder"
        )
    task_name_template_includes_prefix_placeholder = (
        task_name_template.find("{prefix}") != -1
    )

    if not task_name_template_includes_prefix_placeholder and task_name_prefix:
        raise click.UsageError(
            "Task name prefix was set but task name template does not include {prefix} placeholder"
        )
    if not task_name_template.endswith(".cpp") and not ignore_file_extension:
        task_name_template += ".cpp"
    task_file_names = []

    if task_name_template_includes_prefix_placeholder:
        if not task_name_prefix:
            task_name_prefix = DEFAULT_TASK_FILE_NAME_PREFIX
        task_file_names = [
            task_name_template.format(prefix=task_name_prefix, task_num=task_num)
            for task_num in range(1, num_tasks + 1)
        ]
    if not task_file_names:
        task_file_names = [
            task_name_template.format(task_num=task_num)
            for task_num in range(1, num_tasks + 1)
        ]
    for task_file_name in task_file_names:
        if does_file_exist(task_file_name) and not force:
            click.echo(
                f"File {task_file_name} already exists, use --force to overwrite"
            )
            return
    click.echo(f"Generating {num_tasks} tasks")

    payload = None

    if include_iostream:
        payload = TASK_PAYLOAD_WITH_IOSTREAM
    if not payload:
        payload = TASK_PAYLOAD
    with progressbar(task_file_names) as tasks_progress_bar:
        for task_index, task_file_name in enumerate(tasks_progress_bar):
            with open(task_file_name, "w") as task_file:
                task_file.write(payload.format(task_num=task_index + 1))
    click.echo(f"Successfully generated {num_tasks} tasks")


@cli.command()
@click.argument("task_num", type=int)
@click.option("--force", "-f", is_flag=True, help="Overwrite existing file")
@click.option(
    "--ignore-file-extension",
    is_flag=True,
    help="Do not add .cpp extension if a custom task name template does not have it",
)
@click.option(
    "--include-iostream",
    "--io",
    is_flag=True,
    help="Whether to include iostream library in payload",
)
@click.option(
    "--task-name-template",
    "-t",
    type=click.STRING,
    default=DEFAULT_TASK_FILE_NAME,
    help=f'Default: "{DEFAULT_TASK_FILE_NAME}",'
    f" placeholders: {{task_num}} - required, {{prefix}} - optional",
)
@click.option(
    "--task-name-prefix",
    "-p",
    type=click.STRING,
    default=None,
    help=f'Default: "{DEFAULT_TASK_FILE_NAME_PREFIX}"',
)
def generate_single(
    task_num,
    force,
    ignore_file_extension,
    include_iostream,
    task_name_template,
    task_name_prefix,
):
    if task_name_template.find("{task_num}") == -1:
        raise click.UsageError(
            "Task name template has to include {task_num} placeholder"
        )
    task_name_template_includes_prefix_placeholder = (
        task_name_template.find("{prefix}") != -1
    )

    if not task_name_template_includes_prefix_placeholder and task_name_prefix:
        raise click.UsageError(
            "Task name prefix was set but task name template does not include {prefix} placeholder"
        )
    if not task_name_template.endswith(".cpp") and not ignore_file_extension:
        task_name_template += ".cpp"
    task_file_name = ""

    if task_name_template_includes_prefix_placeholder:
        if not task_name_prefix:
            task_name_prefix = DEFAULT_TASK_FILE_NAME_PREFIX
        task_file_name = task_name_template.format(
            prefix=task_name_prefix, task_num=task_num
        )
    if not task_file_name:
        task_file_name = task_name_template.format(task_num=task_num)
    if does_file_exist(task_file_name) and not force:
        click.echo(f"File {task_file_name} already exists, use --force to overwrite")
        return
    click.echo("Generating task")

    payload = None

    if include_iostream:
        payload = TASK_PAYLOAD_WITH_IOSTREAM
    if not payload:
        payload = TASK_PAYLOAD
    with open(task_file_name, "w") as task_file:
        task_file.write(payload.format(task_num=task_num))
    click.echo("Successfully generated task")


@cli.command()
@click.argument(
    "output-file-name",
    type=click.Path(
        dir_okay=False,
        writable=True,
    ),
    default="Solution.txt",
)
@click.option("--force", "-f", is_flag=True, help="Overwrite existing file")
@click.option(
    "--ignore-input-file-extensions",
    is_flag=True,
    help="Do not add .cpp extension if a custom task name template does not have it",
)
@click.option(
    "--ignore-output-file-extension",
    is_flag=True,
    help="Do not add .txt extension if a custom output file name does not have it",
)
@click.option(
    "--ignore-missing-tasks",
    is_flag=True,
    help="Continue operation even if missing tasks are"
    " found (a warning will be shown anyway)",
)
@click.option(
    "--no-padding",
    is_flag=True,
)
@click.option(
    "--centered-task-names",
    "-c",
    is_flag=True,
)
@click.option(
    "--no-bottom-padding",
    is_flag=True,
)
@click.option("--left-padding-length", type=click.INT, default=None)
@click.option(
    "--line-length",
    type=click.INT,
    default=100,
)
@click.option(
    "--task-file-name-template",
    "-t",
    type=click.STRING,
    default=DEFAULT_TASK_FILE_NAME,
    help=f'Default: "{DEFAULT_TASK_FILE_NAME}",'
    f" placeholders: {{task_num}} - required, {{prefix}} - optional",
)
@click.option(
    "--task-file-name-prefix",
    "-p",
    type=click.STRING,
    default=None,
    help=f'Default: "{DEFAULT_TASK_FILE_NAME_PREFIX}"',
)
@click.option(
    "--task-name-template",
    type=click.STRING,
    default=DEFAULT_TASK_NAME,
    help=f'Default: "{DEFAULT_TASK_NAME}",'
    f" placeholders: {{task_num}} - required, {{prefix}} - optional",
)
@click.option(
    "--task-name-prefix",
    type=click.STRING,
    default=None,
    help=f'Default: "{DEFAULT_TASK_NAME_PREFIX}"',
)
def merge(
    output_file_name,
    force,
    ignore_input_file_extensions,
    ignore_output_file_extension,
    ignore_missing_tasks,
    no_padding,
    centered_task_names,
    no_bottom_padding,
    line_length,
    left_padding_length,
    task_file_name_template,
    task_file_name_prefix,
    task_name_template,
    task_name_prefix,
):
    if task_file_name_template.find("{task_num}") == -1:
        raise click.UsageError(
            "Task file name template has to include {task_num} placeholder"
        )
    task_file_name_template_includes_prefix_placeholder = (
        task_file_name_template.find("{prefix}") != -1
    )

    if (
        not task_file_name_template_includes_prefix_placeholder
        and task_file_name_prefix
    ):
        raise click.UsageError(
            "Task file name prefix was set but task name template does not include {prefix} placeholder"
        )
    if task_name_template.find("{task_num}") == -1:
        raise click.UsageError(
            "Task file name template has to include {task_num} placeholder"
        )
    task_name_template_includes_prefix_placeholder = (
        task_file_name_template.find("{prefix}") != -1
    )

    if not task_name_template_includes_prefix_placeholder and task_name_prefix:
        raise click.UsageError(
            "Task file name prefix was set but task name template does not include {prefix} placeholder"
        )
    if (no_padding or centered_task_names) and left_padding_length is not None:
        raise click.UsageError(
            "Left padding length cannot be configured when no padding or"
            " task names centering is used"
        )
    left_padding_length = DEFAULT_LEFT_PADDING_LENGTH

    if not output_file_name.endswith(".txt") and not ignore_output_file_extension:
        output_file_name += ".txt"
    if does_file_exist(output_file_name) and not force:
        click.echo(f"File {output_file_name} already exists, use --force to overwrite")
        return
    if (
        not task_file_name_template.endswith(".cpp")
        and not ignore_input_file_extensions
    ):
        task_file_name_template += ".cpp"
    task_file_name_glob_pattern = ""

    if task_file_name_template_includes_prefix_placeholder:
        if not task_file_name_prefix:
            task_file_name_prefix = DEFAULT_TASK_FILE_NAME_PREFIX
            task_file_name_glob_pattern = task_file_name_template.format(
                prefix=task_file_name_prefix, task_num="[1-9]"
            )
    if not task_file_name_glob_pattern:
        task_file_name_glob_pattern = task_file_name_template.format(prefix=task_file_name_prefix, task_num="[1-9]")
    found_task_file_names = [
        *glob.glob(task_file_name_glob_pattern),
        *glob.glob(task_file_name_glob_pattern.replace("[1-9]", "[1-9][0-9]")),
        *glob.glob(task_file_name_glob_pattern.replace("[1-9]", "[1-9][0-9][0-9]")),
    ]

    number_start_index = task_file_name_glob_pattern.find("[1-9]")

    tasks = []
    task_numbers = []
    for task_name in found_task_file_names:
        task_number = get_first_number_from_string(task_name[number_start_index:])
        tasks.append(Task(task_name, task_number))
        task_numbers.append(task_number)
    if not task_numbers:
        raise click.UsageError("There are no files to merge")
    last_task_number = max(task_numbers)

    missing_tasks = []

    for task_number in range(1, last_task_number + 1):
        if task_number not in task_numbers:
            missing_tasks.append(task_number)
    missing_tasks_count = len(missing_tasks)
    if missing_tasks_count != 0:
        if not ignore_missing_tasks:
            click.echo(f"ERROR: Found {missing_tasks_count} missing tasks: ")
            for index, missing_task_num in enumerate(missing_tasks):
                click.echo(
                    f"#{index + 1} {task_file_name_glob_pattern.replace('[1-9]', str(missing_task_num))}"
                )
            click.echo("If this is intentional run with --ignore-missing-tasks")
            return
        click.echo(f"WARN: Ignoring {missing_tasks_count} missing tasks: ")
        for index, missing_task_num in enumerate(missing_tasks):
            click.echo(
                f"#{index + 1} {task_file_name_glob_pattern.replace('[1-9]', str(missing_task_num))}"
            )
    merged_data = ""

    found_task_file_names_count = len(found_task_file_names)

    compiled_task_name_template = task_name_template

    if task_name_template_includes_prefix_placeholder:
        if not task_name_prefix:
            task_name_prefix = DEFAULT_TASK_NAME_PREFIX
        compiled_task_name_template = task_name_template.format(
            prefix=task_name_prefix, task_num="{task_num}"
        )
    click.echo(f"Merging {found_task_file_names_count} tasks to {output_file_name}")
    with progressbar(tasks) as tasks_progress_bar:
        for task_index, task in enumerate(tasks_progress_bar):
            task_name = compiled_task_name_template.format(task_num=task.number)

            with open(task.filename, "r") as task_file:
                padding_length = line_length - len(task_name)

                if centered_task_names and not no_padding:
                    one_side_padding_length = int(padding_length / 2)
                    one_side_padding = "-" * one_side_padding_length
                    merged_data += f"{one_side_padding}{task_name}{one_side_padding}"
                elif not no_padding:
                    padding_left = "-" * left_padding_length
                    padding_right = "-" * (padding_length - left_padding_length)
                    merged_data += f"{padding_left}{task_name}{padding_right}"
                else:
                    merged_data += task_name
                merged_data += "\n"
                merged_data += task_file.read()

                if not no_padding and not no_bottom_padding:
                    merged_data += "-" * line_length
                    merged_data += "\n"

                if task_index + 1 < found_task_file_names_count:
                    merged_data += "\n"
    with open(output_file_name, "w") as output_file:
        output_file.write(merged_data)
    click.echo(
        f"Successfully merged {found_task_file_names_count} tasks to {output_file_name}"
    )


if __name__ == "__main__":
    cli()
