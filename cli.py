"""
Модуль для работы с сервисом через консоль.
"""
import asyncio

import click

from app.utilities.db_data import base_data


@click.group()
def cli():
    pass


@cli.command('base-data')
def init_base_data():
    """
    Обработчик команды `quart init base-data` - инициализация добавления базовых данных.
    """
    success = asyncio.get_event_loop().run_until_complete(base_data.init_base_data())
    click.echo('Базовые данные - успешно добавлены!' if success else 'Базовые данные - уже существуют!')


if __name__ == '__main__':
    cli()
