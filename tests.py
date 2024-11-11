import unittest
from unittest.mock import patch, mock_open, MagicMock
from shell import Shell
import zipfile
import io


class TestShell(unittest.TestCase):
    def setUp(self):
        # Инициализация Shell с путем к моковому ZIP-архиву
        self.shell = Shell('vfs_test.zip')

    @patch('zipfile.ZipFile')
    def test_ls(self, mock_zip):
        # Мокаем список файлов в ZIP-архиве
        mock_zip.return_value.__enter__.return_value.namelist.return_value = [
            'Goodbye.txt', 'Files/', 'Files/memes/', 'Files/memes/rngsl-1.png', 'Files/text.txt'
        ]
        self.shell.depth = 1
        expected_files = ['Goodbye.txt', 'Files/']
        actual_files = self.shell.ls()
        self.assertEqual(set(actual_files), set(expected_files))

    @patch('zipfile.ZipFile')
    def test_cd(self, mock_zip):
        # Настройка поведения мокового ZIP-архива
        mock_zip.return_value.__enter__.return_value.namelist.return_value = [
            'Goodbye.txt', 'Files/', 'Files/memes/', 'Files/memes/rngsl-1.png', 'Files/text.txt'
        ]
        self.shell.cd('Files')
        self.assertEqual(self.shell.cwd, 'Files/')
        self.assertEqual(self.shell.depth, 2)

    @patch('zipfile.ZipFile')
    @patch('builtins.open', new_callable=mock_open)
    def test_rm(self, mock_file, mock_zip):
        mock_zip.return_value.__enter__.return_value.namelist.return_value = ['Goodbye.txt']
        self.shell.rm('Goodbye.txt')
        mock_zip.return_value.__enter__.return_value.writestr.assert_not_called()

    @patch('zipfile.ZipFile')
    def test_cp(self, mock_zip):
        src_data = "Hello, world!"
        mock_zip.return_value.__enter__.return_value.namelist.return_value = ['Goodbye.txt']
        mock_zip.return_value.__enter__.return_value.open.return_value.__enter__.return_value.read.return_value = src_data

        self.shell.cp('Goodbye.txt', 'Files')

        mock_zip.return_value.__enter__.return_value.writestr.assert_called_with('Files/Goodbye.txt', src_data)


if __name__ == '__main__':
    unittest.main()
