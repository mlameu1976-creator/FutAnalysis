from sqlalchemy import text
from app.database import engine


class MatchesLoader:

    @staticmethod
    def insert_matches(matches):

        conn = engine.raw_connection()
        cursor = conn.cursor()

        for m in matches:

            try:

                cursor.execute(
                    """
                    INSERT INTO matches (
                        external_id,
                        league_id,
                        home_team,
                        away_team,
                        match_date,
                        season,
                        home_goals,
                        away_goals,
                        is_finished
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (external_id) DO NOTHING
                    """,
                    (
                        int(m["external_id"]),
                        int(m["league_id"]),
                        m["home_team"],
                        m["away_team"],
                        m["match_date"],
                        m["season"],
                        m["home_goals"],
                        m["away_goals"],
                        m["is_finished"]
                    )
                )

            except Exception as e:

                print("Erro ao inserir match:", e)

        conn.commit()

        cursor.close()
        conn.close()