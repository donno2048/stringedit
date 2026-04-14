from argparse import ArgumentParser
from prompt_toolkit.shortcuts import choice, input_dialog

try:
    from . import int_gt_one, radix_type, method_type, print_ordered_strings_from_file,\
                  get_sorted_strings_from_file, MaxLengthValidator, replace_all_file, sanitize
except ImportError:
    from stringedit import int_gt_one, radix_type, method_type, print_ordered_strings_from_file,\
                           get_sorted_strings_from_file, MaxLengthValidator, replace_all_file, sanitize

def get_main_arguments() -> ArgumentParser:
    parser = ArgumentParser(description="Replace strings in binary files")
    parser.add_argument("filename", help="input filename")
    parser.add_argument("-n", "--bytes", default=4, type=int_gt_one, metavar="[number]",
                        help="print amy string of at least %(metavar)s characters (default %(default)s)")
    return parser

def get_print_arguments() -> ArgumentParser:
    parser = get_main_arguments()
    parser.description = "Print strings in binary files"
    parser.add_argument("-t", "--radix", type=radix_type, metavar="{o,d,x}",
                        help="print the location of the string in base 8, 10 or 16")
    parser.add_argument("-s", "--output-separator", metavar="<string>",
                        help="string used to separate strings in output")
    return parser

def get_edit_arguments() -> ArgumentParser:
    parser = get_main_arguments()
    parser.add_argument("-m", "--method", default='r', type=method_type, metavar="{l,r,L}",
                        help="method used to widen replacement string if it's too long\n"
                             "l - pad with spaces from the left\n"
                             "r - pad with spaces from the right\n"
                             "L - leave everything after the replacement as it was\n")
    return parser

def print_strings() -> None:
    args = get_print_arguments().parse_args()
    with open(args.filename, "rb") as file:
        print_ordered_strings_from_file(args.bytes, file.fileno(), args.radix, args.output_separator)

def edit_strings() -> None:
    args = get_edit_arguments().parse_args()
    with open(args.filename, "rb+") as file:
        strings = get_sorted_strings_from_file(args.bytes, file.fileno())
        while True:
            string = choice(
                message="The file is loaded please choose a string to edit:",
                options=[(b'', "Save and Exit"), *((string, string.decode()) for string in strings.keys())],
                mouse_support=True
            )
            if not string: break
            replacement = input_dialog(
                title=string.decode(),
                text="Please enter a replacement",
                ok_text="REPLACE",
                validator=MaxLengthValidator(len(string))
            ).run()
            if replacement is not None:
                replace_all_file(strings[string], sanitize(replacement, len(string), args.method).encode(), file.fileno())
                strings[replacement.encode() + string[len(replacement):]] = strings.pop(string)

if __name__ == '__main__':
    edit_strings()
