config = {
    # md 语法规则
    "type": "github",
    # 正则规则
    "pattern": {
        "HEAD": {
            "H1": r"^#{1}\s.*",
            "H2": r"^#{2}\s.*",
            "H3": r"^#{3}\s.*",
            "H4": r"^#{4}\s.*",
            "H5": r"^#{5}\s.*",
            "H6": r"^#{6}\s.*",
        }
    },
    # 常量
    "constant": {
        "HEAD": {
            "H1": {
                "content": "#",
                "level": -1
            },
            "H2": {
                "content": "##",
                "level": -2
            },
            "H3": {
                "content": "###",
                "level": -3
            },
            "H4": {
                "content": "####",
                "level": -4
            },
            "H5": {
                "content": "#####",
                "level": -5
            },
            "H6": {
                "content": "#####",
                "level": -6
            },
        }
    }
}
