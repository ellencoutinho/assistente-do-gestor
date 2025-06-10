class Code:
    output_files = {}

    @staticmethod
    def add_to_file(filename, content):
        if filename not in Code.output_files:
            Code.output_files[filename] = []
        Code.output_files[filename].append(content)
        
    @staticmethod
    def dump():
        for filename, contents in Code.output_files.items():
            with open(filename, 'w', encoding="utf-8") as file:
                file.write("\n".join(contents))