from threadweave.chunker.text_chunker import TextChunker
from threadweave.constants import *


def test_text_chunker():
    text: str = """When Paul Jobs was mustered out of the Coast Guard after World War II, he made a wager with
        his crewmates. They had arrived in San Francisco, where their ship was decommissioned, and
        Paul bet that he would find himself a wife within two weeks. He was a taut, tattooed engine
        mechanic, six feet tall, with a passing resemblance to James Dean. But it wasn’t his looks that got
        him a date with Clara Hagopian, a sweet-humored daughter of Armenian immigrants. It was the
        fact that he and his friends had a car, unlike the group she had originally planned to go out with
        that evening. Ten days later, in March 1946, Paul got engaged to Clara and won his wager. It
        would turn out to be a happy marriage, one that lasted until death parted them more than forty
        years later.
        Paul Reinhold Jobs had been raised on a dairy farm in Germantown, Wisconsin. Even though
        his father was an alcoholic and sometimes abusive, Paul ended up with a gentle and calm
        disposition under his leathery exterior. After dropping out of high school, he wandered through the
        Midwest picking up work as a mechanic until, at age nineteen, he joined the Coast Guard, even
        though he didn’t know how to swim. He was deployed on the USS General M. C. Meigs and spent
        much of the war ferrying troops to Italy for General Patton. His talent as a machinist and fireman
        earned him commendations, but he occasionally found himself in minor trouble and never rose
        above the rank of seaman.
        Clara was born in New Jersey, where her parents had landed after fleeing the Turks in Armenia,
        and they moved to the Mission District of San Francisco when she was a child. She had a secret
        that she rarely mentioned to anyone: She had been married before, but her husband had been
        killed in the war. So when she met Paul Jobs on that first date, she was primed to start a new life.
        Like many who lived through the war, they had experienced enough excitement that, when it
        was over, they desired simply to settle down, raise a family, and lead a less eventful life. They had
        little money, so they moved to Wisconsin and lived with Paul’s parents for a few years, then
        headed for Indiana, where he got a job as a machinist for International Harvester. His passion was
        tinkering with old cars, and he made money in his spare time buying, restoring, and selling them.
        Eventually he quit his day job to become a full-time used car salesman.
        Clara, however, loved San Francisco, and in 1952 she convinced her husband to move back
        there. They got an apartment in the Sunset District facing the Pacific, just south of Golden Gate
        Park, and he took a job working for a finance company as a “repo man,” picking the locks of cars
        whose owners hadn’t paid their loans and repossessing them. He also bought, repaired, and sold
        some of the cars, making a decent enough living in the process.
        There was, however, something missing in their lives. They wanted children, but Clara had
        suffered an ectopic pregnancy, in which the fertilized egg was implanted in a fallopian tube rather
        than the uterus, and she had been unable to have any. So by 1955, after nine years of marriage,
        they were looking to adopt a child.
        Like Paul Jobs, Joanne Schieble was from a rural Wisconsin family of German heritage. Her
        father, Arthur Schieble, had immigrated to the outskirts of Green Bay, where he and his wife
        owned a mink farm and dabbled successfully in various other businesses, including
        real estate and photoengraving. He was very strict, especially regarding his daughter’s
        relationships, and he had strongly disapproved of her first love, an artist who was not a Catholic.
        Thus it was no surprise that he threatened to cut Joanne off completely when, as a graduate student 
        at the University of Wisconsin, she fell in love with Abdulfattah “John” Jandali, a Muslim
        teaching assistant from Syria.
        Jandali was the youngest of nine children in a prominent Syrian family. His father owned oil
        refineries and multiple other businesses, with large holdings in Damascus and Homs, and at one
        point pretty much controlled the price of wheat in the region. His mother, he later said, was a
        “traditional Muslim woman” who was a “conservative, obedient housewife.” Like the Schieble
        family, the Jandalis put a premium on education. Abdulfattah was sent to a Jesuit boarding school,
        even though he was Muslim, and he got an undergraduate degree at the American University in
        Beirut before entering the University of Wisconsin to pursue a doctoral degree in political science.
        In the summer of 1954, Joanne went with Abdulfattah to Syria. They spent two months in
        Homs, where she learned from his family to cook Syrian dishes. When they returned to Wisconsin
        she discovered that she was pregnant. They were both twenty-three, but they decided not to get
        married. Her father was dying at the time, and he had threatened to disown her if she wed
        Abdulfattah. Nor was abortion an easy option in a small Catholic community. So in early 1955,
        Joanne traveled to San Francisco, where she was taken into the care of a kindly doctor who
        sheltered unwed mothers, delivered their babies, and quietly arranged closed adoptions.
        Joanne had one requirement: Her child must be adopted by college graduates. So the doctor
        arranged for the baby to be placed with a lawyer and his wife. But when a boy was born—on
        February 24, 1955—the designated couple decided that they wanted a girl and backed out. Thus it
        was that the boy became the son not of a lawyer but of a high school dropout with a passion for
        mechanics and his salt-of-the-earth wife who was working as a bookkeeper. Paul and Clara named
        their new baby Steven Paul Jobs.
        When Joanne found out that her baby had been placed with a couple who had not even
        graduated from high school, she refused to sign
        the adoption papers. The standoff lasted weeks, even after the baby had settled into the Jobs
        household. Eventually Joanne relented, with the stipulation that the couple promise—indeed sign a
        pledge—to fund a savings account to pay for the boy’s college education.
        There was another reason that Joanne was balky about signing the adoption papers. Her father
        was about to die, and she planned to marry Jandali soon after. She held out hope, she would later
        tell family members, sometimes tearing up at the memory, that once they were married, she could
        get their baby boy back.
        Arthur Schieble died in August 1955, after the adoption was finalized. Just after Christmas that
        year, Joanne and Abdulfattah were married in St. Philip the Apostle Catholic Church in Green
        Bay. He got his PhD in international politics the next year, and then they had another child, a girl
        named Mona. After she and Jandali divorced in 1962, Joanne embarked on a dreamy and
        peripatetic life that her daughter, who grew up to become the acclaimed novelist Mona Simpson,
        would capture in her book Anywhere but Here. Because Steve’s adoption had been closed, it
        would be twenty years before they would all find each other.
        Steve Jobs knew from an early age that he was adopted. “My parents were very open with me
        about that,” he recalled. He had a vivid memory of sitting on the lawn of his house, when he was
        six or seven years old, telling the girl who lived across the street. “So does that mean your real
        parents didn’t want you?” the girl asked. “Lightning bolts went off in my head,” according to
        Jobs. “I remember running into the house, crying. And my parents said, ‘No, you have to
        understand.’ They were very serious and looked me straight in the eye. They said, ‘We
        specifically picked you out.’ Both of my parents said that and repeated it slowly for me. And they
        put an emphasis on every word in that sentence.”
        Abandoned. Chosen. Special. Those concepts became part of who Jobs was and how he
        regarded himself. His closest friends think that the knowledge that he was given up at birth left
        some scars. “I think his desire for complete control of whatever he makes derives directly from his
        personality and the fact that he was abandoned at birth,” said one longtime colleague, Del Yocam.
        “He wants to control his environment,
        and he sees the product as an extension of himself.” Greg Calhoun, who became close to Jobs
        right after college, saw another effect. “Steve talked to me a lot about being abandoned and the 
        pain that caused,” he said. “It made him independent. He followed the beat of a different
        drummer, and that came from being in a different world than he was born into.”
        Later in life, when he was the same age his biological father had been when he abandoned him,
        Jobs would father and abandon a child of his own. (He eventually took responsibility for her.)
        Chrisann Brennan, the mother of that child, said that being put up for adoption left Jobs “full of
        broken glass,” and it helps to explain some of his behavior. “He who is abandoned is an
        abandoner,” she said. Andy Hertzfeld, who worked with Jobs at Apple in the early 1980s, is
        among the few who remained close to both Brennan and Jobs. “The key question about Steve is
        why he can’t control himself at times from being so reflexively cruel and harmful to some
        people,” he said. “That goes back to being abandoned at birth. The real underlying problem was
        the theme of abandonment in Steve’s life.”
        Jobs dismissed this. “There’s some notion that because I was abandoned, I worked very hard so
        I could do well and make my parents wish they had me back, or some such nonsense, but that’s
        ridiculous,” he insisted. “Knowing I was adopted may have made me feel more independent, but I
        have never felt abandoned. I’ve always felt special. My parents made me feel special.” He would
        later bristle whenever anyone referred to Paul and Clara Jobs as his “adoptive” parents or implied
        that they were not his “real” parents. “They were my parents 1,000%,” he said. When speaking
        about his biological parents, on the other hand, he was curt: “They were my sperm and egg bank.
        That’s not harsh, it’s just the way it was, a sperm bank thing, nothing more.”
        Silicon Valley
        The childhood that Paul and Clara Jobs created for their new son was, in many ways, a stereotype
        of the late 1950s. When Steve was two they adopted a girl they named Patty, and three years later
        they moved to a tract house in the suburbs. The finance company where Paul worked as a repo
        man, CIT, had transferred him down to its Palo Alto office, but he could not afford to live there,
        so they landed in a subdivision in Mountain View, a less expensive town just to the south.
        There Paul tried to pass along his love of mechanics and cars. “Steve, this is your workbench
        now,” he said as he marked off a section of the table in their garage. Jobs remembered being
        impressed by his father’s focus on craftsmanship. “I thought my dad’s sense of design was pretty
        good,” he said, “because he knew how to build anything. If we needed a cabinet, he would build
        it. When he built our fence, he gave me a hammer so I could work with him.”
        Fifty years later the fence still surrounds the back and side yards of the house in Mountain
        View. As Jobs showed it off to me, he caressed the stockade panels and recalled a lesson that his
        father implanted deeply in him. It was important, his father said, to craft the backs of cabinets and
        fences properly, even though they were hidden. “He loved doing things right. He even cared about
        the look of the parts you couldn’t see.”
        His father continued to refurbish and resell used cars, and he festooned the garage with pictures
        of his favorites. He would point out the detailing of the design to his son: the lines, the vents, the
        chrome, the trim of the seats. After work each day, he would change into his dungarees and retreat
        to the garage, often with Steve tagging along. “I figured I could get him nailed down with a little
        mechanical ability, but he really wasn’t interested in getting his hands dirty,” Paul later recalled.
        “He never really cared too much about mechanical things.”
        “I wasn’t that into fixing cars,” Jobs admitted. “But I was eager to hang out with my dad.” Even
        as he was growing more aware that he had been adopted, he was becoming more attached to his
        father. One day when he was about eight, he discovered a photograph of his father from his time
        in the Coast Guard. “He’s in the engine room, and he’s got his shirt off and looks like James Dean.
        It was one of those Oh wow moments for a kid. Wow, oooh, my parents were actually once very
        young and really good-looking.”
        Through cars, his father gave Steve his first exposure to electronics. “My dad did not have a
        deep understanding of electronics, but he’d
        encountered it a lot in automobiles and other things he would fix. He showed me the rudiments
        of electronics, and I got very interested in that.” Even more interesting were the trips to scavenge
        for parts. “Every weekend, there’d be a junkyard trip. We’d be looking for a generator, a
        carburetor, all sorts of components.” He remembered watching his father negotiate at the counter. 
        “He was a good bargainer, because he knew better than the guys at the counter what the parts
        should cost.” This helped fulfill the pledge his parents made when he was adopted. “My college
        fund came from my dad paying $50 for a Ford Falcon or some other beat-up car that didn’t run,
        working on it for a few weeks, and selling it for $250—and not telling the IRS.”
        The Jobses’ house and the others in their neighborhood were built by the real estate developer
        Joseph Eichler, whose company spawned more than eleven thousand homes in various California
        subdivisions between 1950 and 1974. Inspired by Frank Lloyd Wright’s vision of simple modern
        homes for the American “everyman,” Eichler built inexpensive houses that featured floor-toceiling glass walls, open floor plans, exposed post-and-beam construction, concrete slab floors,
        and lots of sliding glass doors. “Eichler did a great thing,” Jobs said on one of our walks around
        the neighborhood. “His houses were smart and cheap and good. They brought clean design and
        simple taste to lower-income people. They had awesome little features, like radiant heating in the
        floors. You put carpet on them, and we had nice toasty floors when we were kids.”
        Jobs said that his appreciation for Eichler homes instilled in him a passion for making nicely
        designed products for the mass market. “I love it when you can bring really great design and
        simple capability to something that doesn’t cost much,” he said as he pointed out the clean
        elegance of the houses. “It was the original vision for Apple. That’s what we tried to do with the
        first Mac. That’s what we did with the iPod.”
        Across the street from the Jobs family lived a man who had become successful as a real estate
        agent. “He wasn’t that bright,” Jobs recalled, “but he seemed to be making a fortune. So my dad
        thought, ‘I can do that.’ He worked so hard, I remember. He took these night classes, passed the
        license test, and got into real estate. Then the bottom fell out
        of the market.” As a result, the family found itself financially strapped for a year or so while
        Steve was in elementary school. His mother took a job as a bookkeeper for Varian Associates, a
        company that made scientific instruments, and they took out a second mortgage. One day his
        fourth-grade teacher asked him, “What is it you don’t understand about the universe?” Jobs
        replied, “I don’t understand why all of a sudden my dad is so broke.” He was proud that his father
        never adopted a servile attitude or slick style that may have made him a better salesman. “You had
        to suck up to people to sell real estate, and he wasn’t good at that and it wasn’t in his nature. I
        admired him for that.” Paul Jobs went back to being a mechanic.
        His father was calm and gentle, traits that his son later praised more than emulated. He was also
        resolute. Jobs described one example:
        Nearby was an engineer who was working at Westinghouse. He was a single guy, beatnik type. He had
        a girlfriend. She would babysit me sometimes. Both my parents worked, so I would come here right
        after school for a couple of hours. He would get drunk and hit her a couple of times. She came over one
        night, scared out of her wits, and he came over drunk, and my dad stood him down—saying “She’s
        here, but you’re not coming in.” He stood right there. We like to think everything was idyllic in the
        1950s, but this guy was one of those engineers who had messed-up lives.
        What made the neighborhood different from the thousands of other spindly-tree subdivisions
        across America was that even the ne’er-do-wells tended to be engineers. “When we moved here,
        there were apricot and plum orchards on all of these corners,” Jobs recalled. “But it was beginning
        to boom because of military investment.” He soaked up the history of the valley and developed a
        yearning to play his own role. Edwin Land of Polaroid later told him about being asked by
        Eisenhower to help build the U-2 spy plane cameras to see how real the Soviet threat was. The
        film was dropped in canisters and returned to the NASA Ames Research Center in Sunnyvale, not
        far from where Jobs lived. “The first computer terminal I ever saw was when my dad brought me
        to the Ames Center,” he said. “I fell totally in love with it.”
        Other defense contractors sprouted nearby during the 1950s. The Lockheed Missiles and Space
        Division, which built submarine-launched ballistic missiles, was founded in 1956 next to the
        NASA Center; by the time Jobs moved to the area four years later, it employed twenty thousand
        people. A few hundred yards away, Westinghouse built facilities that produced tubes and
        electrical transformers for the missile systems. “You had all these military companies on the
        cutting edge,” he recalled. “It was mysterious and high-tech and made living here very exciting.”

        """
    chunker = TextChunker()
    chunks = chunker.create_chunks(text)

    for ch in chunks:
        print(ch)
        assert (
            len(ch) <= DEFAULT_CHUNK_SIZE +2
        ), f"Chunk size is invalid, {len(ch)} : DEFAULT: {DEFAULT_CHUNK_SIZE}"
