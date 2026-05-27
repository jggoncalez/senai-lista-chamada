import uuid

from app.database import SessionLocal
from app.models.role import Role
from app.models.usuario import Usuario
from app.models.curso import Curso
from app.models.turma import Turma
from app.models.aluno import Aluno
from app.models.turma_disciplina import TurmaDisciplina
from app.models.sessao_aula import SessaoAula
from app.models.presenca import PresencaAluno
from app.models.aluno_disciplina_extra import AlunoDisciplinaExtra


def limpar(db):
    print("🗑️  Limpando banco...")
    db.query(PresencaAluno).delete()
    db.query(SessaoAula).delete()
    db.query(AlunoDisciplinaExtra).delete()
    db.query(TurmaDisciplina).delete()
    db.query(Aluno).delete()
    db.query(Turma).delete()
    db.query(Curso).delete()
    db.query(Usuario).delete()
    db.query(Role).delete()
    db.commit()
    print("✅ Banco limpo!")


def seed():
    db = SessionLocal()
    try:
        limpar(db)

        # ── Roles ────────────────────────────────────────────────
        print("👤 Criando roles...")
        role_professor = Role(nome="professor")
        role_coord = Role(nome="coordenador")
        role_admin = Role(nome="admin")
        db.add_all([role_professor, role_coord, role_admin])
        db.flush()

# ── Usuários ─────────────────────────────────────────────
        print("👤 Criando usuários...")
        professores = [
            Usuario(nome="Prof. João Silva",     email="joao.silva@senai.com.br",     role_id=role_professor.id, azure_object_id=str(uuid.uuid4())),
            Usuario(nome="Prof. Maria Oliveira", email="maria.oliveira@senai.com.br", role_id=role_professor.id, azure_object_id=str(uuid.uuid4())),
            Usuario(nome="Prof. Carlos Souza",   email="carlos.souza@senai.com.br",   role_id=role_professor.id, azure_object_id=str(uuid.uuid4())),
            Usuario(nome="Prof. Ana Lima",       email="ana.lima@senai.com.br",       role_id=role_professor.id, azure_object_id=str(uuid.uuid4())),
            Usuario(nome="Coord. Roberto Alves", email="roberto.alves@senai.com.br",  role_id=role_coord.id,     azure_object_id=str(uuid.uuid4())),
            Usuario(nome="Admin SENAI",          email="admin@senai.com.br",          role_id=role_admin.id,     azure_object_id=str(uuid.uuid4())),
        ]
        db.add_all(professores)
        db.flush()
        p_joao, p_maria, p_carlos, p_ana = professores[0], professores[1], professores[2], professores[3]

        # ── Cursos/Disciplinas ───────────────────────────────────
        print("📚 Criando cursos e disciplinas...")
        cursos = [
            # Desenvolvimento de Sistemas
            Curso(nome="Lógica de Programação",           carga_horaria=80,  eixo_tecnologico="TIC",           duracao_termos=1),
            Curso(nome="Programação Orientada a Objetos", carga_horaria=80,  eixo_tecnologico="TIC",           duracao_termos=2),
            Curso(nome="Banco de Dados",                  carga_horaria=60,  eixo_tecnologico="TIC",           duracao_termos=2),
            Curso(nome="Desenvolvimento Web",             carga_horaria=80,  eixo_tecnologico="TIC",           duracao_termos=3),
            # Mecânica
            Curso(nome="Metrologia",                      carga_horaria=60,  eixo_tecnologico="Manufatura",    duracao_termos=1),
            Curso(nome="Processos de Usinagem",           carga_horaria=120, eixo_tecnologico="Manufatura",    duracao_termos=2),
            Curso(nome="Resistência dos Materiais",       carga_horaria=80,  eixo_tecnologico="Manufatura",    duracao_termos=3),
            Curso(nome="Desenho Técnico Mecânico",        carga_horaria=60,  eixo_tecnologico="Manufatura",    duracao_termos=1),
            # Eletroeletrônica
            Curso(nome="Circuitos Elétricos",             carga_horaria=80,  eixo_tecnologico="Energia",       duracao_termos=1),
            Curso(nome="Eletrônica Analógica",            carga_horaria=80,  eixo_tecnologico="Energia",       duracao_termos=2),
            Curso(nome="Sistemas Digitais",               carga_horaria=60,  eixo_tecnologico="Energia",       duracao_termos=2),
            Curso(nome="Automação Industrial",            carga_horaria=100, eixo_tecnologico="Energia",       duracao_termos=3),
        ]
        db.add_all(cursos)
        db.flush()

        c_logica, c_poo, c_bd, c_web = cursos[0], cursos[1], cursos[2], cursos[3]
        c_metro, c_usinagem, c_resist, c_desenho = cursos[4], cursos[5], cursos[6], cursos[7]
        c_circuitos, c_analogica, c_digitais, c_automacao = cursos[8], cursos[9], cursos[10], cursos[11]

        # ── Turmas ───────────────────────────────────────────────
        print("🏫 Criando turmas...")
        turmas = [
            # Desenvolvimento de Sistemas
            Turma(cod_turma="3DEVT", nome_turma="Desenvolvimento de Sistemas 3A", curso_id=c_poo.id,       termo=3),
            Turma(cod_turma="2DEVT", nome_turma="Desenvolvimento de Sistemas 2A", curso_id=c_logica.id,    termo=2),
            Turma(cod_turma="1DEVT", nome_turma="Desenvolvimento de Sistemas 1A", curso_id=c_logica.id,    termo=1),
            # Mecânica
            Turma(cod_turma="3MECT", nome_turma="Mecânica Industrial 3A",         curso_id=c_resist.id,    termo=3),
            Turma(cod_turma="2MECT", nome_turma="Mecânica Industrial 2A",         curso_id=c_usinagem.id,  termo=2),
            Turma(cod_turma="1MECT", nome_turma="Mecânica Industrial 1A",         curso_id=c_metro.id,     termo=1),
            # Eletroeletrônica
            Turma(cod_turma="3ELET", nome_turma="Eletroeletrônica 3A",            curso_id=c_automacao.id, termo=3),
            Turma(cod_turma="2ELET", nome_turma="Eletroeletrônica 2A",            curso_id=c_analogica.id, termo=2),
            Turma(cod_turma="1ELET", nome_turma="Eletroeletrônica 1A",            curso_id=c_circuitos.id, termo=1),
        ]
        db.add_all(turmas)
        db.flush()

        t_3dev, t_2dev, t_1dev = turmas[0], turmas[1], turmas[2]
        t_3mec, t_2mec, t_1mec = turmas[3], turmas[4], turmas[5]
        t_3ele, t_2ele, t_1ele = turmas[6], turmas[7], turmas[8]

        # ── Alunos ───────────────────────────────────────────────
        print("🎓 Criando alunos...")
        def criar_alunos(turma, nomes, empresas, ra_inicio):
            return [
                Aluno(
                    turma_id=turma.id,
                    nome=nome,
                    empresa=empresas[i % len(empresas)],
                    ra=str(ra_inicio + i).zfill(4),
                    ativo=True
                )
                for i, nome in enumerate(nomes)
            ]

        alunos_3dev = criar_alunos(t_3dev, [
            "Ana Paula Silva", "Bruno Costa", "Carlos Eduardo",
            "Diana Souza", "Eduardo Lima", "Fernanda Oliveira",
            "Gabriel Santos", "Helena Martins", "Igor Pereira", "Julia Rocha"
        ], ["TechCorp", "DevBrasil", "InovaTI", "Softex"], 1001)

        alunos_2dev = criar_alunos(t_2dev, [
            "Lucas Almeida", "Mariana Ferreira", "Nicolas Barbosa",
            "Olivia Castro", "Pedro Henrique", "Rafaela Nunes",
            "Samuel Torres", "Tatiane Moura"
        ], ["TechCorp", "DevBrasil", "StartupXYZ"], 2001)

        alunos_1dev = criar_alunos(t_1dev, [
            "Alice Rodrigues", "Bernardo Lima", "Clara Mendes",
            "Davi Carvalho", "Emilly Santos", "Felipe Araujo",
            "Giovana Pires", "Henrique Costa"
        ], ["InovaTI", "Softex", "DevBrasil"], 3001)

        alunos_3mec = criar_alunos(t_3mec, [
            "André Machado", "Beatriz Cunha", "César Figueiredo",
            "Daniela Ramos", "Elias Correia", "Flávia Monteiro",
            "Gustavo Teixeira", "Isabela Freitas", "João Vitor Lopes", "Karen Vieira"
        ], ["MetalPeças", "IndústriaMec", "AçosBrasil"], 4001)

        alunos_2mec = criar_alunos(t_2mec, [
            "Leonardo Brito", "Melissa Campos", "Nathan Silveira",
            "Patricia Gomes", "Rafael Cardoso", "Simone Ribeiro",
            "Thiago Nascimento", "Vanessa Moreira"
        ], ["MetalPeças", "TorneariaPrecisa"], 5001)

        alunos_1mec = criar_alunos(t_1mec, [
            "Arthur Dias", "Bruna Esteves", "Caio Fernandes",
            "Débora Guimarães", "Emanuel Henrique", "Fabiana Ito",
            "Guilherme Jardim", "Hanna Kato"
        ], ["AçosBrasil", "IndústriaMec"], 6001)

        alunos_3ele = criar_alunos(t_3ele, [
            "Ian Lacerda", "Juliana Melo", "Kevin Nogueira",
            "Larissa Oliveira", "Mateus Pacheco", "Natalia Queiroz",
            "Otávio Rezende", "Paula Siqueira", "Quintino Torres", "Renata Ulhoa"
        ], ["ElétricaSP", "AutomaçãoPro", "EletroTech"], 7001)

        alunos_2ele = criar_alunos(t_2ele, [
            "Sergio Vasconcelos", "Tânia Wanderley", "Ulisses Xavier",
            "Vera Yamamura", "Wagner Zanetti", "Xuxa Albuquerque",
            "Yuri Bastos", "Zilda Cavalcanti"
        ], ["ElétricaSP", "CircuitosBR"], 8001)

        alunos_1ele = criar_alunos(t_1ele, [
            "Alan Drummond", "Bianca Evangelista", "Cristian Falcão",
            "Denise Galvão", "Enzo Herrera", "Fabio Inácio",
            "Graziela Jacinto", "Humberto Keller"
        ], ["AutomaçãoPro", "EletroTech"], 9001)

        todos_alunos = (
            alunos_3dev + alunos_2dev + alunos_1dev +
            alunos_3mec + alunos_2mec + alunos_1mec +
            alunos_3ele + alunos_2ele + alunos_1ele
        )
        db.add_all(todos_alunos)
        db.flush()

        # ── TurmaDisciplinas ─────────────────────────────────────
        print("📋 Criando turma-disciplinas...")
        turma_disciplinas = [
            # Desenvolvimento
            TurmaDisciplina(turma_id=t_3dev.id, curso_id=c_poo.id,      professor_id=p_joao.id,   dia_semana=0),
            TurmaDisciplina(turma_id=t_3dev.id, curso_id=c_bd.id,       professor_id=p_maria.id,  dia_semana=2),
            TurmaDisciplina(turma_id=t_3dev.id, curso_id=c_web.id,      professor_id=p_joao.id,   dia_semana=4),
            TurmaDisciplina(turma_id=t_2dev.id, curso_id=c_logica.id,   professor_id=p_maria.id,  dia_semana=1),
            TurmaDisciplina(turma_id=t_2dev.id, curso_id=c_bd.id,       professor_id=p_joao.id,   dia_semana=3),
            TurmaDisciplina(turma_id=t_1dev.id, curso_id=c_logica.id,   professor_id=p_maria.id,  dia_semana=0),
            # Mecânica
            TurmaDisciplina(turma_id=t_3mec.id, curso_id=c_resist.id,   professor_id=p_carlos.id, dia_semana=1),
            TurmaDisciplina(turma_id=t_3mec.id, curso_id=c_usinagem.id, professor_id=p_carlos.id, dia_semana=3),
            TurmaDisciplina(turma_id=t_2mec.id, curso_id=c_metro.id,    professor_id=p_carlos.id, dia_semana=0),
            TurmaDisciplina(turma_id=t_2mec.id, curso_id=c_desenho.id,  professor_id=p_ana.id,    dia_semana=2),
            TurmaDisciplina(turma_id=t_1mec.id, curso_id=c_metro.id,    professor_id=p_carlos.id, dia_semana=4),
            TurmaDisciplina(turma_id=t_1mec.id, curso_id=c_desenho.id,  professor_id=p_ana.id,    dia_semana=1),
            # Eletroeletrônica
            TurmaDisciplina(turma_id=t_3ele.id, curso_id=c_automacao.id,  professor_id=p_ana.id,  dia_semana=2),
            TurmaDisciplina(turma_id=t_3ele.id, curso_id=c_digitais.id,   professor_id=p_ana.id,  dia_semana=4),
            TurmaDisciplina(turma_id=t_2ele.id, curso_id=c_analogica.id,  professor_id=p_ana.id,  dia_semana=0),
            TurmaDisciplina(turma_id=t_2ele.id, curso_id=c_circuitos.id,  professor_id=p_ana.id,  dia_semana=3),
            TurmaDisciplina(turma_id=t_1ele.id, curso_id=c_circuitos.id,  professor_id=p_ana.id,  dia_semana=1),
        ]
        db.add_all(turma_disciplinas)
        db.commit()

        print("✅ Seed concluído!")
        print(f"   → {len(todos_alunos)} alunos")
        print(f"   → {len(turmas)} turmas")
        print(f"   → {len(cursos)} disciplinas")
        print(f"   → {len(turma_disciplinas)} turma-disciplinas")
        print(f"   → {len(professores)} usuários")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro no seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()