INSERT INTO companies (name, country, founded_year, website, description) VALUES
    ('Nintendo', 'Japan', 1889, 'https://www.nintendo.com', 'Japanese multinational video game company known for iconic franchises like Mario, Zelda, and Pokémon.'),
    ('Ubisoft', 'France', 1986, 'https://www.ubisoft.com', 'French video game publisher known for Assassin''s Creed, Far Cry, and Rainbow Six.'),
    ('CD Projekt', 'Poland', 1994, 'https://www.cdprojekt.com', 'Polish game developer and publisher known for The Witcher series and Cyberpunk 2077.'),
    ('Valve Corporation', 'USA', 1996, 'https://www.valvesoftware.com', 'American video game developer and digital distribution company, creator of Steam, Half-Life, and Dota 2.'),
    ('FromSoftware', 'Japan', 1986, 'https://www.fromsoftware.jp', 'Japanese video game developer known for Souls series, Sekiro, and Elden Ring.')
ON CONFLICT (name) DO NOTHING;

INSERT INTO teams (name, specialty, size, description, company_id) VALUES
    ('EPD Production Group No. 1', 'Development', 120, 'Responsible for Nintendo Switch sports and ring-fit games.', (SELECT id FROM companies WHERE name = 'Nintendo')),
    ('EPD Production Group No. 3', 'Development', 200, 'Developed Breath of the Wild and Tears of the Kingdom.', (SELECT id FROM companies WHERE name = 'Nintendo')),
    ('NST', 'Studio', 80, 'Nintendo Software Technology, US-based dev team.', (SELECT id FROM companies WHERE name = 'Nintendo')),

    ('Ubisoft Montreal', 'Development', 4000, 'Largest game studio in the world, led many AAA titles.', (SELECT id FROM companies WHERE name = 'Ubisoft')),
    ('Ubisoft Paris', 'Development', 800, 'Co-developed multiple Assassin''s Creed titles.', (SELECT id FROM companies WHERE name = 'Ubisoft')),
    ('Ubisoft Online Services', 'Infrastructure', 300, 'Handles all online infrastructure and live services.', (SELECT id FROM companies WHERE name = 'Ubisoft')),

    ('CD Projekt RED', 'Development', 1200, 'Main development studio behind The Witcher and Cyberpunk 2077.', (SELECT id FROM companies WHERE name = 'CD Projekt')),
    ('GOG', 'Publishing', 250, 'Digital game distribution platform focusing on DRM-free games.', (SELECT id FROM companies WHERE name = 'CD Projekt')),
    ('QA Department', 'Quality Assurance', 300, 'Internal QA team for all CD Projekt titles.', (SELECT id FROM companies WHERE name = 'CD Projekt')),

    ('Steam Platform Team', 'Platform', 200, 'Develops and maintains the Steam gaming platform.', (SELECT id FROM companies WHERE name = 'Valve Corporation')),
    ('Hardware Team', 'Hardware', 150, 'Responsible for Steam Deck and Index VR headset.', (SELECT id FROM companies WHERE name = 'Valve Corporation')),
    ('Game Development', 'Development', 100, 'Works on Valve''s own game titles.', (SELECT id FROM companies WHERE name = 'Valve Corporation')),

    ('Soulsborne Team', 'Development', 300, 'Core team behind Dark Souls, Bloodborne, and Elden Ring.', (SELECT id FROM companies WHERE name = 'FromSoftware')),
    ('Armored Core Team', 'Development', 150, 'Team dedicated to the Armored Core mecha series.', (SELECT id FROM companies WHERE name = 'FromSoftware')),
    ('Sound & Music', 'Audio', 40, 'Creates the iconic soundscapes and music of FromSoftware games.', (SELECT id FROM companies WHERE name = 'FromSoftware'))
ON CONFLICT DO NOTHING;
