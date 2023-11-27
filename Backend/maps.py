from os import path


class MapManager:
    def __init__(self, map_name):
        self.map_name = map_name
        self.map_list = []
        self.path = path.join("Backend\Maps", f"{self.map_name}.rin")

    def overwrite_map(self):
        with open(self.path, 'w') as file:
            for line in reversed(self.map_list):
                file.writelines(f"{str(line)}\n")

    def convert_to_map_list(self, circle_list: list, time: int):
        current_circle_list = [" ", " ", " ", " ", ""]
        for num in circle_list:
            current_circle_list[num] = "O"
        current_circle_list[len(current_circle_list) - 1] = f"{self.add_decimal(time)}s"
        self.map_list.append(current_circle_list)

    def import_map(self):
        self.map_list.clear()
        if not path.exists(self.path):
            raise Exception("File Not Found")
        with open(self.path, "r") as map_file:
            for lines in map_file:
                self.map_list.append(lines.strip())
        return reversed(self.map_list)

    def reset_map_list(self) -> None:
        self.map_list.clear()

    @staticmethod
    def add_decimal(num: int):
        if len(num_string := str(num)) == 1:
            return num_string + ".00"
        elif len(num_string) == 2:
            return num_string + ".0"
        else:
            return num_string + " "


if __name__ == "__main__":
    map1 = MapManager("jujutsu")
    map1.overwrite_map()
