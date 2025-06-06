# services/google_sheets.py
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from typing import List, Any
import asyncio
from config.settings import config
from config.constants import TRAINING_COLORS, format_date

class GoogleSheetsService:
    def __init__(self):
        self.credentials = Credentials.from_service_account_file(
            config.CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.spreadsheet_id = "19oLEXKWJMmV1KMCUhQjnGZu1VLaQlfMvl3ALLiTvHRI"

    async def append_row(self, training_data: dict) -> bool:
        try:
            # Форматируем данные для записи
            row_data = [
                format_date(),  # Дата
                training_data['training_type_name'],  # Тип тренировки
                f"{training_data['distance']:.2f} км",  # Расстояние
                f"{training_data['time']:.2f}",  # Время
                training_data['pace'],  # Темп
                f"{training_data['pulse']} уд/мин",  # Пульс
                training_data.get('additional_info', '-'),  # Доп. информация
                training_data.get('feelings', '-')  # Ощущения
            ]

            # Выполняем запись в отдельном потоке
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,
                self._append_row_sync,
                row_data,
                training_data['training_type']
            )
            return result
        except Exception as e:
            print(f"Error appending row: {e}")
            return False

    def _append_row_sync(self, row_data: List[Any], training_type: str) -> bool:
        try:
            # Добавляем данные
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{config.SHEET_NAME}!A:H",
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body={'values': [row_data]}
            ).execute()

            # Получаем номер добавленной строки
            updated_range = result.get('updates', {}).get('updatedRange', '')
            if not updated_range:
                return False

            # Применяем форматирование
            if training_type in TRAINING_COLORS:
                self._format_row(
                    updated_range,
                    TRAINING_COLORS[training_type]
                )

            return True
        except Exception as e:
            print(f"Error in _append_row_sync: {e}")
            return False

    def _format_row(self, range_name: str, color: dict):
        try:
            # Получаем номер строки из диапазона
            row_number = int(range_name.split('!A')[1].split(':')[0])

            format_request = {
                'requests': [{
                    'updateCells': {
                        'rows': [{
                            'values': [{
                                'userEnteredFormat': {
                                    'backgroundColor': color,
                                    'horizontalAlignment': 'CENTER',
                                    'verticalAlignment': 'MIDDLE',
                                    'textFormat': {'fontSize': 10}
                                }
                            }] * 8  # Применяем ко всем 8 ячейкам строки
                        }],
                        'fields': 'userEnteredFormat',
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': row_number - 1,
                            'endRowIndex': row_number,
                            'startColumnIndex': 0,
                            'endColumnIndex': 8
                        }
                    }
                }]
            }

            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=format_request
            ).execute()

        except Exception as e:
            print(f"Error formatting row: {e}")

    def get_table_url(self) -> str:
        """Возвращает URL таблицы"""
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"

sheets_service = GoogleSheetsService()
