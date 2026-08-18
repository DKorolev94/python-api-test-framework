from typing import Self

from sshtunnel import SSHTunnelForwarder

from src.utils.logger import get_logger

logger = get_logger(__name__)


class SSHTunnel:
    """SSH туннель, пробрасывающий один или несколько удалённых портов на localhost.

    Универсальный класс, не привязан к конкретному сервису. Подходит для БД,
    Kafka, ClickHouse и любого другого хоста, доступного только через SSH jump box.
    """

    def __init__(
        self,
        ssh_host: str,
        ssh_port: int,
        ssh_user: str,
        ssh_pkey: str,
        remote_binds: list[tuple[str, int]],
    ):
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_pkey = ssh_pkey
        self.remote_binds = remote_binds
        self.forwarder: SSHTunnelForwarder | None = None

    def start(self) -> SSHTunnelForwarder:
        """Открывает SSH соединение и запускает проброс удалённых портов."""
        self.forwarder = SSHTunnelForwarder(
            (self.ssh_host, self.ssh_port),
            ssh_username=self.ssh_user,
            ssh_pkey=self.ssh_pkey,
            remote_bind_addresses=self.remote_binds,
            set_keepalive=30,
        )
        self.forwarder.start()
        logger.info(f"SSH tunnel started: {self.remote_binds} -> {self.forwarder.local_bind_ports}")
        return self.forwarder

    @property
    def local_bind_ports(self) -> list[int]:
        """Локальные порты 127.0.0.1, по одному на каждый удалённый порт, в том же порядке."""
        return self.forwarder.local_bind_ports

    def stop(self) -> None:
        """Закрывает SSH соединение, если оно было открыто."""
        if self.forwarder:
            self.forwarder.stop()

    def __enter__(self) -> Self:
        """Запускает туннель и возвращает self."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Останавливает туннель при выходе из контекста."""
        self.stop()
