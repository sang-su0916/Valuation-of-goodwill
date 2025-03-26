const express = require('express');
const router = express.Router();
const Valuation = require('../models/Valuation');

// 모든 평가 내역 조회
router.get('/', async (req, res) => {
  try {
    const valuations = await Valuation.find().sort({ evaluationDate: -1 });
    res.json(valuations);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// 새로운 평가 생성
router.post('/', async (req, res) => {
  const valuation = new Valuation(req.body);
  try {
    const newValuation = await valuation.save();
    res.status(201).json(newValuation);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// 특정 평가 조회
router.get('/:id', async (req, res) => {
  try {
    const valuation = await Valuation.findById(req.params.id);
    if (valuation) {
      res.json(valuation);
    } else {
      res.status(404).json({ message: '평가를 찾을 수 없습니다.' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// 평가 수정
router.patch('/:id', async (req, res) => {
  try {
    const valuation = await Valuation.findById(req.params.id);
    if (valuation) {
      Object.assign(valuation, req.body);
      const updatedValuation = await valuation.save();
      res.json(updatedValuation);
    } else {
      res.status(404).json({ message: '평가를 찾을 수 없습니다.' });
    }
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// 평가 삭제
router.delete('/:id', async (req, res) => {
  try {
    const valuation = await Valuation.findById(req.params.id);
    if (valuation) {
      await valuation.remove();
      res.json({ message: '평가가 삭제되었습니다.' });
    } else {
      res.status(404).json({ message: '평가를 찾을 수 없습니다.' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router; 