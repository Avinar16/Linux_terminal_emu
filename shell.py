import zipfile
import os


class Shell:
    def __init__(self, vfs_path):
        self.vfs_path = vfs_path
        self.cwd = ''  # начинаем с корневой директории
        self.depth = 1

    def ls(self):
        content_list = []
        with zipfile.ZipFile(self.vfs_path, 'r') as z:
            print(z.namelist())
            for item in z.namelist():
                if len(set(item.split('/')) - {''}) == self.depth:
                    content_list.append(item[len(self.cwd):])

        return list(set(content_list))

    def cd(self, target_dir):
        if target_dir == '..':
            if self.cwd != '/':
                self.cwd = '/'.join(self.cwd.rstrip('/').split('/')[:-1])
        elif target_dir == '/':
            self.cwd = ''
            self.depth = 1
        else:
            new_path = os.path.join(self.cwd, target_dir).replace('\\', '/')
            if not new_path.endswith('/'):
                new_path += '/'
            with zipfile.ZipFile(self.vfs_path, 'r') as z:
                if any(x.startswith(new_path) for x in z.namelist()):
                    self.cwd = new_path
                    self.depth = new_path.count('/') + 1

    def rm(self, filename):
        new_zip_content = []
        file_removed = False
        with zipfile.ZipFile(self.vfs_path, 'r') as z:
            new_zip_content = [item for item in z.namelist() if item != filename]
            file_removed = len(new_zip_content) != len(z.namelist())
        if file_removed:
            with zipfile.ZipFile(self.vfs_path, 'w') as new_z:
                for item in new_zip_content:
                    new_z.write(item)

    def cp(self, src, dest):
        dest_path = self.cwd + dest
        if not dest_path.endswith('/'):
            dest_path += '/'
        dest_path += src
        print(dest_path)
        with zipfile.ZipFile(self.vfs_path, 'a') as z:
            if src in z.namelist():
                with z.open(src) as src_file:
                    data = src_file.read()
                    z.writestr(dest_path, data)

    def exit(self):
        exit(0)
