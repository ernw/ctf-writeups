function make_board(A0_0)
  local L1_1
  L1_1 = {}
  L1_1.size = A0_0
  setmetatable(L1_1, {
    __tostring = board_tostring
  })
  for _FORV_5_ = 0, A0_0 * A0_0 - 1 do
    L1_1[_FORV_5_] = 0
  end
  return L1_1
end
function populate_board(A0_2, A1_3, A2_4)
  local L3_5, L4_6
  L3_5 = A0_2.size
  if A2_4 then
    L4_6 = math
    L4_6 = L4_6.randomseed
    L4_6(A2_4)
  end
  if not A1_3 then
    L4_6 = L3_5 * L3_5
    L4_6 = L4_6 * 3
    A1_3 = L4_6 / 4
  end
  function L4_6()
    repeat
    until A0_2[math.random(L3_5 * L3_5) - 1] == 0
    return math.random(L3_5 * L3_5) - 1
  end
  if A1_3 > 0 then
    for _FORV_8_, _FORV_9_ in ipairs({
      "a",
      "b",
      "c",
      "d"
    }) do
      A0_2[L4_6()] = _FORV_9_
    end
    for _FORV_8_ = 1, A1_3 - 4 do
      A0_2[L4_6()] = math.random(4)
    end
    return fall(A0_2)
  end
end
function board_tostring(A0_7)
  local L1_8, L2_9, L3_10, L4_11, L5_12, L6_13, L7_14
  L1_8 = {}
  L2_9 = A0_7.size
  for L6_13 = 0, L2_9 - 1 do
    L7_14 = "|"
    for _FORV_11_ = 0, L2_9 - 1 do
      L7_14 = L7_14 .. " " .. A0_7[_FORV_11_ + L6_13 * L2_9]
    end
    _FOR_.insert(L1_8, L7_14 .. " |")
  end
  return L3_10(L4_11, L5_12)
end
function fall(A0_15)
  local L1_16, L2_17, L3_18, L4_19, L5_20, L6_21, L7_22
  L1_16 = A0_15.size
  L2_17 = make_board
  L3_18 = L1_16
  L2_17 = L2_17(L3_18, L4_19)
  function L3_18(A0_23)
    local L1_24, L3_25, L4_26, L5_27, L6_28, L7_29
    L1_24 = L1_16
    L1_24 = L1_24 - 1
    for L6_28 = L3_25 - 1, 0, -1 do
      L7_29 = L1_16
      L7_29 = L6_28 * L7_29
      L7_29 = L7_29 + A0_23
      L7_29 = A0_15[L7_29]
      if L7_29 ~= 0 then
        L7_29 = L1_16
        L7_29 = L1_24 * L7_29
        L7_29 = L7_29 + A0_23
        L2_17[L7_29] = A0_15[L6_28 * L1_16 + A0_23]
        L1_24 = L1_24 - 1
      end
    end
  end
  for L7_22 = 0, L1_16 - 1 do
    L3_18(L7_22)
  end
  return L2_17
end
function rotate(A0_30)
  local L1_31
  L1_31 = A0_30.size
  for _FORV_6_ = 0, L1_31 - 1 do
    for _FORV_11_ = 0, L1_31 - 1 do
      make_board(L1_31, 0)[_FORV_11_ * L1_31 + (L1_31 - 1 - _FORV_6_)] = A0_30[_FORV_6_ * L1_31 + _FORV_11_]
    end
  end
  return (make_board(L1_31, 0))
end
function crush(A0_32)
  local L1_33
  L1_33 = A0_32.size
  for _FORV_7_ = 0, L1_33 - 1 do
    make_board(L1_33, 0)[_FORV_7_] = A0_32[_FORV_7_]
  end
  for _FORV_7_ = L1_33, L1_33 * L1_33 - 1 do
    if A0_32[_FORV_7_ - L1_33] == ({
      "a",
      "b",
      "c",
      "d"
    })[A0_32[_FORV_7_]] then
      make_board(L1_33, 0)[_FORV_7_] = 0
    else
      make_board(L1_33, 0)[_FORV_7_] = A0_32[_FORV_7_]
    end
  end
  return (make_board(L1_33, 0))
end
function rotate_left(A0_34)
  local L1_35, L2_36
  L1_35 = rotate
  L2_36 = rotate
  L2_36 = L2_36(rotate(A0_34))
  return L1_35(L2_36, L2_36(rotate(A0_34)))
end
function readAll(A0_37)
  io.open(A0_37, "rb"):close()
  return (io.open(A0_37, "rb"):read("*all"))
end
function help()
  local L0_38
  L0_38 = string
  L0_38 = L0_38.sub
  L0_38 = L0_38(readAll("server.luac"), 2)
  writeraw(L0_38, string.len(L0_38))
end
quit = false
function exit()
  local L0_39, L1_40
  quit = true
end
function run_step(A0_41)
  local L1_42, L2_43
  L1_42 = readline
  L1_42 = L1_42()
  L2_43 = string
  L2_43 = L2_43.len
  L2_43 = L2_43(L1_42)
  if L2_43 == 0 then
    L2_43 = exit
    L2_43()
    L2_43 = nil
    return L2_43
  end
  L2_43 = string
  L2_43 = L2_43.find
  L2_43 = L2_43(L1_42, "function")
  if L2_43 then
    L2_43 = nil
    return L2_43
  end
  L2_43 = string
  L2_43 = L2_43.find
  L2_43 = L2_43(L1_42, "print")
  if L2_43 then
    L2_43 = nil
    return L2_43
  end
  L2_43 = load
  L2_43 = L2_43("return " .. L1_42)
  L2_43 = L2_43()
  if L2_43 == nil then
    return nil
  end
  return L2_43(A0_41)
end
function game()
  local L0_44
  L0_44 = populate_board
  L0_44 = L0_44(make_board(8))
  repeat
    writeline(board_tostring(L0_44) .. "\n")
    if not quit then
      if run_step(L0_44) ~= nil then
        L0_44 = run_step(L0_44)
        L0_44 = fall(crush(fall(L0_44)))
      else
        writeline("Didn't understand. Type 'rotate', 'rotate_left', 'exit', or 'help'.\n")
      end
    end
  until false
end
writeline("let's play a game\n")
game()
