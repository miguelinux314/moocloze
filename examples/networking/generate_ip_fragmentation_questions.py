#!/usr/bin/env python3
"""Generate questions about IP datagram fragmentation for importing from Moodle.

Created for class "104353 Computer networks and internet" at the
Universitat Autònoma de Barcelona (UAB).
"""
__author__ = "Miguel Hernández-Cabronero"
__since__ = "2024/03/15"

import os
import random
import moocloze


def generate_fragmentation_questions():
    """Generate fragmentation questions. A datagram travels through two networks with different
    MTUs and is fragmented. Questions are split into small-to-large and large-to-small MTUs.
    """
    large_to_small_questions = []
    small_to_large_questions = []

    mtu_sizes = [50, 60, 85, 121]
    net1_fragment_count_list = [3, 4]

    for mtu_net1 in mtu_sizes:
        for mtu_net2 in mtu_sizes:
            if mtu_net2 == mtu_net1:
                continue
            for net1_fragment_count in net1_fragment_count_list:
                # Net 1
                # full fragments
                n1_data_lengths = [8 * ((mtu_net1 - 20) // 8)] * (net1_fragment_count - 1)
                # last fragment
                n1_data_lengths.append(random.randint(1, mtu_net1 - 20))
                # data offsets
                n1_offsets = [sum(n1_data_lengths[:i]) for i in range(len(n1_data_lengths))]
                # total lengths
                n1_total_lengths = [l + 20 for l in n1_data_lengths]
                # original datagram data length before (potential) fragmentation
                original_datagram_data_length = n1_offsets[-1] + n1_data_lengths[-1]

                # Net 2
                n2_data_lengths = []
                n2_offsets = []
                n2_total_lengths = []
                for n1_data_length, n1_offset in zip(n1_data_lengths, n1_offsets):
                    last_n1_fragment = (n1_offset == n1_offsets[-1])

                    consumed_fragment_data = 0
                    while consumed_fragment_data < n1_data_length:
                        last_n2_fragment = last_n1_fragment and (
                                (n1_data_length - consumed_fragment_data) <= mtu_net2 - 20)
                        subfragment_data_length = min(n1_data_length - consumed_fragment_data,
                                                      mtu_net2 - 20)
                        if not last_n2_fragment:
                            subfragment_data_length = 8 * (subfragment_data_length // 8)

                        n2_data_lengths.append(subfragment_data_length)
                        n2_offsets.append(n1_offset + consumed_fragment_data)
                        n2_total_lengths.append(subfragment_data_length + 20)

                        consumed_fragment_data += subfragment_data_length

                # Sanity checks
                assert all(l <= mtu_net1 for l in n1_total_lengths)
                assert all(l <= mtu_net2 for l in n2_total_lengths)
                assert all(offset % 8 == 0 for offset in n1_offsets)
                assert all(offset % 8 == 0 for offset in n2_offsets)
                assert n1_offsets == sorted(n1_offsets)
                assert n2_offsets == sorted(n2_offsets)
                assert all(n1_offsets[i] == sum(n1_data_lengths[:i])
                           for i in range(1, len(n1_data_lengths)))
                assert all(n2_offsets[i] == sum(n2_data_lengths[:i])
                           for i in range(1, len(n2_data_lengths)))
                assert (n1_offsets[0] == 0)
                assert (n2_offsets[0] == 0)
                assert sum(n1_data_lengths) == sum(n2_data_lengths)
                assert sum(n1_data_lengths) <= 2 ** 16 - 1
                assert (n1_offsets[-1] + n1_data_lengths[-1]
                        == n2_offsets[-1] + n2_data_lengths[-1])
                assert sum(n1_data_lengths) == original_datagram_data_length
                assert sum(n2_data_lengths) == original_datagram_data_length
                assert original_datagram_data_length <= 2 ** 16 - 1

                # Question definition
                header_length = 20
                question = moocloze.Question(
                    name=
                    f"Fragmentation of {original_datagram_data_length} data bytes for MTUs "
                    f"{mtu_net1} and {mtu_net2}",
                    contents=
                    f"An IP datagram D with total size "
                    f"{original_datagram_data_length + header_length} bytes, "
                    f"which contains {header_length} header bytes, is "
                    f"sent from a node in a network N1 (MTU={mtu_net1}) "
                    f"to another node in a network N2 (MTU={mtu_net2}). "
                    f"N1 and N2 are connected to different interfaces of the same router."
                    f"<br/><br/><ul>"
                    f"<li>What are the 3 smaller fragment data offsets (in bytes) observed in N1 "
                    f"corresponding to D? "
                    f"{moocloze.Numerical(answer=n1_offsets[0])} &lt;"
                    f"{moocloze.Numerical(answer=n1_offsets[1])} &lt;"
                    f"{moocloze.Numerical(answer=n1_offsets[2])} "
                    f"</li>"
                    f"<li>What are the 3 largest fragment data offsets (in bytes) observed in N2 "
                    f"corresponding to D? "
                    f"{moocloze.Numerical(answer=n2_offsets[-3])} &lt;"
                    f"{moocloze.Numerical(answer=n2_offsets[-2])} &lt;"
                    f"{moocloze.Numerical(answer=n2_offsets[-1])} "
                    f"</li>"
                    f"<li>How many fragments corresponding to D are observed in N1 with the "
                    f"'More Fragments' flag set to 1? "
                    f"{moocloze.Numerical(answer=len(n1_offsets) - 1)}"
                    f"</li>"
                    f"<li>How many fragments corresponding to D are observed in N2 with the "
                    f"'More Fragments' flag set to 0? "
                    f"{moocloze.Numerical(answer=1)}"
                    f"</li>"
                    f"</ul>",
                    general_feedback=
                    "Did you get them all right?<br/><ul>"
                    f"<li>In N1, the sorted fragment data offsets are: "
                    f"{', '.join(str(o) for o in n1_offsets)}</li>"
                    f"<li>In N2, the sorted fragment data offsets are: "
                    f"{', '.join(str(o) for o in n2_offsets)}</li>"
                    "</ul>"
                    "Of course, only the last fragment in each network has the MF flag set to 0."
                    + ("<br/>Also remember that only the destination host "
                       "(and never the intermediate routers) reconstruct the "
                       "data fragments." if mtu_net1 < mtu_net2 else "")
                )

                if mtu_net1 < mtu_net2:
                    small_to_large_questions.append(question)
                else:
                    large_to_small_questions.append(question)

    moocloze.questions_to_xml_file(small_to_large_questions,
                                   os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "small_to_large_mtu_fragmentation.xml"))
    moocloze.questions_to_xml_file(large_to_small_questions,
                                   os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "large_to_small_mtu_fragmentation.xml"))


if __name__ == "__main__":
    random.seed(0xd34dc0ff)
    generate_fragmentation_questions()
