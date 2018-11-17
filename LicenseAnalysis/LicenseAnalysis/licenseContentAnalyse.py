def contentAnalysis(text):
    """
    Extract and analysis the license info in the text
    :param text: a long string, the content of a file
    :return: a dict, the license info
    """
    print(text)
    # your analysis process

    result = {
        "licenseNo": 1,
        "textStartPos": 20,
        "textEndPos": 30,
        "versionStartPos": 33,
        "versionEndPos": 35
    }
    return result
