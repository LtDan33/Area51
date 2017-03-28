package HackerRank;

import HackerRank.CTCISection.Balanced;
import org.junit.Assert;
import org.junit.Test;

/**
 * Created by Dan on 03/13/17.
 */
public class BalancedTest {

    @Test
    public void testIt() {

//        {[{((({}{({({()})()})[]({()[[][][]]}){}}))){}}]}{}{({((){{}[][]{}[][]{}}[{}])(())}[][])}
//        ()[[][()[]][]()](([[[(){()[[]](([]))}]]]))
//        ()[]({}{})(()){{{}}()()}({[]()}())[](){}(({()}[{}[{({{}}){({}){({})((({()})))}}}]]))
//        }[{){({}({)})]([}{[}}{[(([])[(}){[]])([]]}(]]]]{][
//        [{]{[{(){[}{}(([(]}])(){[[}(]){(})))}}{{)}}{}][({(}))]}({)
//        )})[(]{][[())]{[]{{}}[)[)}[]){}](}({](}}}[}{({()]]
//        [[[({[]}({[][[[[][[{(()[][])}()[][]][]{}]]]]}))][(()){}]]]()[{}([]{}){}{{}}]
//        ({[]({[]})}())[][{}[{{(({{{([{}])}}}))}}]]
//        ([((()))()])[][][]{}()(([]))[]()[]((){}[]){}(){{}[]}[[{[]}]]
//        [[(((({}{[]{}()}){}{{}}){({[]{[{}]{(){}(((){()}))}()}}[[]]()()[()])[[{}{}]()]}))]]{}[]{}({({{}})})
//        (]{()}((
//        [][(())[({{{()[]}}{[[][[][[[]{{{[()]{{{{}{[]}[][]}}}}}}]]]]}})]]
//        }[})})}[)]{}{)
//        ({(}{})))}(}[)[}{)}}[)[{][{(}{{}]({}{[(})[{[({{[}{(]]})}
//        ]}})[]))]{][])[}(])]({[]}[]([)
//        [{{}{[{{[}[[}([]
//        [([]){}][({})({[(([])[][])][[{}{([{{}{(()){{{({}{{}}())}}[]}}()[()[{{{([](()){[[[]]]})}}}]]}])}]]})]
//        ]{}{(}))}](})[{]]()(]([}]([}][}{]{[])}{{{]([][()){{})[{({{{[}{}](]}}
//        {[{}}){(}[][)(}[}][)({[[{]}[(()[}}){}{)([)]}(()))]{)(}}}][
//        (]{}{(}}}[)[
//        []{}{[[]]}([{}]{}[]){{(())}}
//        [)([{(][(){)[)}{)]]}}([((][[}}(]{}]]}]][(({{{))[[){}{]][))[]{]][)[{{}{()]){)])))){{{[(]}[}}{}]
//        {({(){[[[][]{}[[([]{})]{}]][[]()()]]}})}[{}{{}}]
//        )}][(})){))[{}[}
//        {[]{({]}[}}[{([([)([){{}{(}}[]}}[[{[}[[()(])[}[]
//        ()()()[]
//        ((){}])][]][}{]{)]]}][{]}[)(])[}[({(
//        )[((])(]]]]((]){{{{())]}]}(}{([}(({}]])[[{){[}]{{}})[){(
//        }][[{[((}{[]){}}[[[)({[)}]]}(]]{[)[]}{}(){}}][{()]))})]][(((}}
//        ([]){}{{}{}}()([([{}{[[]()([(([]()))()[[]]])]}])])
//        [()[[]{{[]}()([])}[]][][]][]()[]{}{}[][]{}{}[()(){}]
//        {[{){]({(((({](]{([])([{{([])[}(){(]](]{[{[]}}())[){})}))[{})))[
//        {}[()[]][]{}{}[[{{[[({})]()[[()]]]}}]]
//        {[{}[][]]}[((()))][]({})[]{}{()}
//        (){[{({})}]}
//        ([]])][{)]({)[]))}]())[}]))][}{(}}})){]}]{[)}(][})[[
//        ((({{}(([{}(())]))[()]{[[[]()]]}})))
//        }()))}(}]]{{})}][{](]][{]{[[]]]}]]}([)({([))[[(]}])}[}(([{)[)]]([[](]}]}{]{{})[]){]}{])(
//        {}{}{}{[[()]][]}
//        )]}]({{})[[[{]{{{}}][))]{{
//        ))){({}])}])}}]{)()(}(]}([
//        ([[]][])[[]()][]()(([[]]{[()[]{[][{}]}[()]]{}{[]}}{{}()}(()[([][]{})[[{}][]]{}[]])))
//        (]{[({}[){)))}]{[{}][({[({[]))}[}]}{()(([]{]()}})}[]{[)](((]]])([]}}]){)(([]]}[[}[
//        ([[]])({}(([(){{}[{}]}]){[{}]}))[][{}{}](){}
//        [][][][][][([])][]{({()}[[()()]{([(){[]{}}{(())}{[](){}()({}())}[({}[[]()])][]])}])}
//        }[{{(}})}}(((())()({]{([]((][(({)[({[]]}[])}]{][{{}]{)][}(])}}}))}}}
//        []({})()[]{}{}[]({}{})[]{([])()[()][{()({})[{}{[[()]{}[]][]}(({{[]{()()()}{}[]()}[]}){{}{}})]}]}
//        {{(([{)]{}({][{](){({([[[][)}[)})(
//        [{}]{[()({[{}]})]}
//        [[{}]]
//        ]{{({[{]}[[)]]}{}))}{){({]]}{]([)({{[]){)]{}){){}()})(]]{{])(])[]}][[()()}
//        {[([}[[{{(]]][}()())]{){(){)]]){})}]{][][(}[]())[}[)})})[][{[)[})()][]))}[[}
//        ]()])}[}}}{]]{)[}(}]]])])}{(}{([{]({)]}])(})[{}[)]])]}[]{{)){}{()}]}((}}{({])[}])[]}
//        (]}[{}{{][}))){{{([)([[])([]{[
//        {(()[]){}}(){[]}({{}(()())})([]){}{}(())()[()]{}()
//        {{}[{}[{}[]]]}{}({{[]}})[[(){}][]]{}(([]{[][]()()}{{{()()}{[]}({}[]{()})}{()}[[]][()]}))
//        {[][]}[{}[](){}]{{}{[][{}]}}
//        ()(){}(){((){}[])([[]]())}
//        {}[[{[((}[(}[[]{{]([(}]][[
//        {}[([{[{{}()}]{}}([[{}[]]({}{{()}[][][]})])])]
//        {[](}([)(])[]]})()]){[({]}{{{)({}(][{{[}}(]{
//        [][]{{}[](())}{}({[()]}())[][[][({}([{}]))]]
//        ((()))[]{[(()({[()({[]}{})]}))]}{[]}{{({}{})[{}{}]{()([()])[{()}()[[]{}()]{}{}[]()]}[[]{[]}([])]}}

        Assert.assertTrue(Balanced.Solution("[()][{}()][](){}([{}(())([[{}]])][])[]([][])(){}{{}{[](){}}}()[]({})[{}{{}([{}][])}]"));
        Assert.assertTrue(Balanced.Solution("[()][{}[{}[{}]]][]{}[]{}[]{{}({}(){({{}{}[([[]][[]])()]})({}{{}})})}"));
        Assert.assertFalse(Balanced.Solution("(])[{{{][)[)])(]){(}))[{(})][[{)(}){[(]})[[{}(])}({)(}[[()}{}}]{}{}}()}{({}](]{{[}}(([{]"));
        Assert.assertFalse(Balanced.Solution("){[]()})}}]{}[}}})}{]{](]](()][{))])(}]}))(}[}{{)}{[[}[]"));
        Assert.assertFalse(Balanced.Solution("}(]}){"));
        Assert.assertFalse(Balanced.Solution("((]()(]([({]}({[)){}}[}({[{])(]{()[]}}{)}}]]{({)[}{("));
        Assert.assertTrue(Balanced.Solution("{}{({{}})}[][{{}}]{}{}(){{}[]}{}([[][{}]]())"));
        Assert.assertTrue(Balanced.Solution("(){}[()[][]]{}(())()[[([])][()]{}{}(({}[]()))()[()[{()}]][]]"));
        Assert.assertTrue(Balanced.Solution("()([]({}[]){}){}{()}[]{}[]()(()([[]]()))()()()[]()(){{}}()({[{}][]}[[{{}({({({})})})}]])"));
        Assert.assertFalse(Balanced.Solution("[]([{][][)(])}()([}[}(})}])}))]](}{}})[]({{}}))[])(}}[[{]{}]()[(][])}({]{}[[))[[}[}{(]})()){{(]]){]["));
        Assert.assertTrue(Balanced.Solution("{()({}[[{}]]()(){[{{}{[[{}]{}((({[]}{}()[])))]((()()))}(()[[[]]])((()[[](({([])()}))[]]))}]})}"));
        Assert.assertTrue(Balanced.Solution("()(){{}}[()()]{}{}"));
        Assert.assertTrue(Balanced.Solution("{}()([[]])({}){({[][[][[()]]{{}[[]()]}]})}[](())((())[{{}}])"));
        Assert.assertTrue(Balanced.Solution("{}(((){}){[]{{()()}}()})[]{{()}{(){()(){}}}}{()}({()(()({}{}()((()((([])){[][{()}{}]})))))})"));
        Assert.assertFalse(Balanced.Solution("][[{)())))}[)}}}}[{){}()]([][]){{{{{[)}]]{([{)()][({}[){]({{"));
        Assert.assertFalse(Balanced.Solution("{{}("));
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertFalse(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
//        Assert.assertTrue(Balanced.Solution("
        
        
    }
}
