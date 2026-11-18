from lib.contrato import RepositorioPedidos
from lib.modelo import Pedido


class RepositorioSQLite(RepositorioPedidos):
    """Implementação concreta; todo o SQL fica nesta classe."""

    def __init__(self, conexao):
        self._conexao = conexao  # emprestada; a montagem fecha a conexão
        with conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    numero INTEGER PRIMARY KEY,
                    item   TEXT    NOT NULL,
                    setor  TEXT    NOT NULL,
                    valor  REAL    NOT NULL CHECK (valor > 0)
                )
            """)

    def adicionar(self, pedido: Pedido) -> bool:
        with self._conexao:
            cursor = self._conexao.execute("""
                INSERT INTO pedidos (numero, item, setor, valor) VALUES (?, ?, ?, ?)
                ON CONFLICT (numero) DO NOTHING
            """, (pedido.numero, pedido.item, pedido.setor, pedido.valor))
        return cursor.rowcount == 1

    def buscar(self, numero: int) -> Pedido | None:
        linha = self._conexao.execute(
            "SELECT numero, item, setor, valor FROM pedidos WHERE numero = ?", (numero,)
        ).fetchone()
        return Pedido(*linha) if linha else None

    def ultimo_numero(self) -> int:
        return self._conexao.execute(
            "SELECT COALESCE(MAX(numero), 0) FROM pedidos"
        ).fetchone()[0]

    def faturamento_por_setor(self) -> dict[str, float]:
        linhas = self._conexao.execute(
            "SELECT setor, SUM(valor) FROM pedidos GROUP BY setor ORDER BY setor"
        ).fetchall()
        return dict(linhas)
