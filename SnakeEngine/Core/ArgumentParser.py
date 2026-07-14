import argparse


def ParseArguments():
    parser = argparse.ArgumentParser(
        description="Snake Engine",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    api_group = parser.add_mutually_exclusive_group()
    api_group.add_argument(
        "-api",
        "--backend",
        action="store",
        choices=["opengl", "vk", "vulkan", "headless"],
        default="opengl",
        help="Backend to use",
    )
    parser.add_argument(
        "-w", "--width", type=int, default=1280, help="Width of the main window"
    )
    parser.add_argument(
        "-H", "--height", type=int, default=720, help="Height of the main window"
    )
    parser.add_argument(
        "-f", "--fullscreen", action="store_true", help="Start in fullscreen mode"
    )

    args, _ = parser.parse_known_args()
    return args
