# Fat BOTtomed Girls (FBG) - 2025 Eurobot Project

[![Tests for Big Bot](https://github.com/NJurquet/FBG/actions/workflows/big_bot_tests.yml/badge.svg)](https://github.com/NJurquet/FBG/actions/workflows/big_bot_tests.yml)

## Overview

**[Eurobot](https://www.eurobot.org/eurobot-contest/)** is an international robotics competition created in France.
The main goal of this event is to encourage youth to practice robotics with fun, by offering them an unforgettable technical and human experience.

Each year, a new theme is defined and the rules are adapted accordingly, with original actions to perform and a **100% self-made robot to build**.
Robots have to be **autonomous** and must be able to perform various tasks on a playing field in a limited amount of time to gather points.
2 teams play against each other by earning as much points as possible.
Aside from the main robot, teams can build SIMAs (Small Independent Mobile Actuator), which are small autonomous robots only living during the last 15 seconds of the match.

Project management, task sharing, autonomy, team spirit and experimentation are the core values to achieve one’s project and be ready to compete on the D-Day.

The Belgian competition was held in **Mons** and hosted by **[SparkOH!](https://sparkoh.be/projet-robotixs/robotixs/)** on April 19-20, 2025.

### Theme

The 2025 theme is **The Show Must Go On!**:

> This year the robots want to do even more competitions, more matches for more fun, but this comes with a cost.
> And in order to raise the necessary funds, some big charity concerts are planned: the Robot-Rock-Tour!
> But putting on a show is a lot of work and that’s why the robots are working extra hard to finish the preparations as quickly as possible, so that the show can take place on time.

![Playground of the 2025 Eurobot competition](docs/playmat_2025.png)

### Points

To score points, the main robot can perform the following actions:

-   **ENSURE THE PROMOTION OF THE SHOW [20 pts]**: Deploy a banner in front of the playground table.
-   **PREPARE THE CONCERT HALL**: Build tribunes of different levels (represented by 1 plank and 2 cans).
    -   [4 pts] per level 1 tribune.
    -   [8 pts] per level 2 tribune.
    -   [16 pts] per level 3 tribune.
-   **STORE TOOLS [10 pts]**: Being in the finishing area at the end of the match.
-   **ESTIMATE THE ENTRIES**: Bonus points earned by displaying an estimated score. The lower the difference between the estimated score and the real score (not counting SIMA score), the more points are earned:

    `Bonus = min(20 points - Delta/2, score done)`

SIMAs can perform the following actions:

-   [5 pts] The superstar is valid on stage at the end of the match.
-   [0, 1, 2, 3, 5, 9 or 15 pts] The superstar is close to the stage edge at the end of the match.
-   [5 pts] For each of the 3 areas of the pit occupied by at least one team groupie at the end of the match.
-   [10 pts] All SIMAs make the party (moving actuator).

## Outcome

### Qualification Round

30 teams participated in the Belgian competition, 15 being from Belgium and 15 from other countries.
The other 15 were from France and Switzerland as guests such that they can test their robots before their national competitions.

The qualification round consist of playing 4 matches against any of the teams and collecting as much cumulative points as possible.

Our team finished **4th out of the 15 Belgian teams** and **7th out of the 30 teams**.
| General Ranking | Belgian Ranking | Team Name | Team Origin | Score |
|-----------------|-----------------|--------------------|------------------|-------|
| 1 | - | Les Karibous | France | 312 |
| 2 | 1 | UCLouvain- Bot save the queen | Belgium | 307 |
| 3 | - | SUDRIABOTIK | France | 304 |
| 4 | 2 | Gramme'N Roll | Belgium | 285 |
| 5 | - | Goldorak | France | 244 |
| 6 | 3 | UCLouvain - WaltiBot | Belgium | 239 |
| **7** | **4** | **ECAM - Fat BOTtomed Girl** | **Belgium** | **238** |
| 7 | - | Coffee Machine | France | 238 |
| 9 | 5 | MonSymphony | Belgium | 235 |
| 10 | 6 | Galil'HELHa | Belgium | 180 |
| 11 | - | Robot ESEO | France | 163 |
| 12 | - | Cybernétique en Nord | France | 158 |
| 13 | - | Evolutek | France | 132 |
| 14 | - | CRENIM | France | 130 |
| 15 | 7 | ECAM - Freddie Carte Mercurie | Belgium | 124 |
| 16 | 8 | Starbot | Belgium | 118 |
| 17 | 9 | ECAM - Johnny Wall-EDay | Belgium | 99 |
| 18 | 10 | ECAM - Daft Bot's | Belgium | 92 |
| 19 | - | RTFM | Switzerland | 73 |
| 20 | - | PM-ROBOTIX | France | 71 |
| 21 | 11 | PAGACH IESN | Belgium | 50 |
| 22 | 12 | UCLouvain - Juke Bot | Belgium | 45 |
| 23 | 13 | UCLouvain - EltonBot | Belgium | 32 |
| 24 | - | TDS-Team Robotique 72 | France | 29 |
| 25 | - | E.S.C.Ro.C.S. | France | 28 |
| 26 | 14 | ECAM - Les Spice Bots | Belgium | 17 |
| 26 | 14 | UCLouvain - GOATBOT | Belgium | 17 |

### Final Round

Being in the top 8 Belgian teams, we made it to the quarter finals.
Our team faced the incredible work of **MonSymphony** who won the championship, ending our journey in the quarter finals.

![Result graph of the 2025 Belgium Eurobot competition](docs/eurobot_2025_belgium_finals.png)

## Project

The repository contains the code used for the SIMAs (Superstar & Groupies) in the [SIMA](./SIMA) folder and the code used for the main robot in the [BIG_BOT](./BIG_BOT) folder.

SIMAs were developed using simple `Arduino` components and coded in `C++`/`Arduino`.
The main robot was developed using a Raspberry Pi 4 to control most of the tasks, hardware, and robotic logic in `Python`.

## License

This project is licensed under the MIT License.
