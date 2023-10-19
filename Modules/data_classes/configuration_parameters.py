from dataclasses import dataclass, field


__all__ = ['Configuracoes']


@dataclass
class Configuracoes:
    cor_da_borda: str = 'darkgreen'
    cor_de_fundo: str = 'lightgreen'
    fonte: str = 'Arial'
    tamanho_texto: int = 8
    tamanho_titulo: int = 10
    fonte_estilo: str = 'bold'
    tipos: list[str] = field(default_factory=lambda: [
        'Multipla escolha 1 correta', 'Multipla escolha n corretas', 'Verdadeiro ou falso'
    ])
    unidades: list[str] = field(default_factory=lambda: [
        'Astec', 'Comunicação', 'Controle de acesso', 'Energia', 'Exportação', 'Gestão', 'Incêndio e iluminação',
        'Negócios', 'Redes', 'Segurança eletrônica', 'Solar', 'Soluções', 'Varejo', 'Verticais'
    ])
    dificuldades: list[str] = field(default_factory=lambda: ['Fácil', 'Médio', 'Difícil'])
